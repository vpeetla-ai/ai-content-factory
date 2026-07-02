"""Pipeline Service — LangGraph runner, streaming, persistence."""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agents.context import get_root_trace_id, get_run_id, set_run_context
from agents.llm import register_run_metrics, unregister_run_metrics
from app.core.cancel_registry import cancel_run as mark_cancelled
from app.core.cancel_registry import is_cancelled
from app.core.checkpointer import ensure_graph_initialized, get_graph
from app.core.config import get_settings
from app.core.database import async_session_factory
from app.core.pipeline_events import publish_pipeline_event
from app.core.redis import get_redis
from app.core.redis_keys import HITL_PENDING, PIPELINE_STATE, PUBLISH_QUEUE
from app.models import ContentDraft, PipelineRun, PipelineStatus, Platform, PublishedPost, User
from app.services.publisher import PublisherService
from app.core.logging import get_logger
from app.vpeetla_observability.context import bind_trace_context, clear_trace_context
from app.vpeetla_observability.export import export_trace_summary
from app.vpeetla_observability.recorder import TraceRecorder, set_recorder
from app.vpeetla_observability.spans import system_span

GRAPH_NODES = frozenset({"research", "content", "enrich", "hitl", "publish"})

NODE_OUTPUT_KEYS = {
    "research": "research_brief",
    "content": "platform_drafts",
    "enrich": "seo_data",
    "hitl": "hitl_approved",
    "publish": "published_results",
}


class PipelineService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _graph(self):
        return get_graph()

    async def create_run(
        self,
        user_id: uuid.UUID,
        topic: str,
        platforms: list[str],
        config: dict | None = None,
    ) -> PipelineRun:
        run_id = uuid.uuid4()
        thread_id = str(run_id)

        run = PipelineRun(
            id=run_id,
            user_id=user_id,
            topic=topic,
            status=PipelineStatus.running,
            langgraph_run_id=thread_id,
        )
        self.db.add(run)
        await self.db.flush()
        return run

    async def execute_run(
        self,
        run_id: uuid.UUID,
        *,
        platforms: list[str] | None = None,
        config: dict | None = None,
        resume: bool = False,
        hitl_approved: dict | None = None,
        hitl_edits: dict | None = None,
    ) -> None:
        result = await self.db.execute(select(PipelineRun).where(PipelineRun.id == run_id))
        run = result.scalar_one_or_none()
        if not run:
            return

        thread_id = run.langgraph_run_id or str(run.id)
        run_id_str = str(run.id)
        trace_id = run_id_str

        await ensure_graph_initialized()
        graph = self._graph()

        if is_cancelled(run_id_str):
            run.status = PipelineStatus.error
            run.state_snapshot = {**(run.state_snapshot or {}), "error": "Cancelled"}
            run.completed_at = datetime.now(UTC)
            await self.db.flush()
            return

        metrics = RunMetrics()
        register_run_metrics(run_id_str, metrics)
        recorder = TraceRecorder.create(run_id=run_id_str, trace_id=trace_id, service=settings.app_name)
        set_recorder(recorder)
        set_run_context(run_id_str, trace_id=trace_id)
        bind_trace_context(run_id=run_id_str, trace_id=trace_id, root_trace_id=trace_id)
        recorder.ensure_langfuse_root("content_factory.pipeline", metadata={"topic": run.topic})

        redis = get_redis()
        await redis.set(PIPELINE_STATE.format(run_id=run_id_str), "running", ex=settings.pipeline_state_ttl)

        graph_config = {"configurable": {"thread_id": thread_id}}
        graph_input: dict | None

        if resume:
            await graph.aupdate_state(
                graph_config,
                {"hitl_approved": hitl_approved or {}, "hitl_edits": hitl_edits or {}},
            )
            graph_input = None
            run.status = PipelineStatus.running
        else:
            snap = run.state_snapshot or {}
            platform_list = platforms or snap.get("platforms") or [p.value for p in Platform]
            graph_input = {
                "topic": run.topic,
                "platforms": platform_list,
                "config": config or snap.get("config") or {},
                "run_id": thread_id,
                "trace_id": trace_id,
            }

        active_nodes: set[str] = set()

        try:
            with system_span("pipeline.execute", run_id=run_id_str, resume=resume):
                async for event in graph.astream_events(
                    graph_input,
                    graph_config,
                    version="v2",
                ):
                    if is_cancelled(run_id_str):
                        raise asyncio.CancelledError("Pipeline cancelled")

                    kind = event.get("event")
                    meta = event.get("metadata") or {}
                    node_name = meta.get("langgraph_node") or event.get("name", "")

                    if kind == "on_chain_start" and node_name in GRAPH_NODES:
                        active_nodes.add(node_name)
                        metrics.start_node(node_name)
                        logger.info("graph_node_started", node=node_name, run_id=run_id_str)
                        await ws.emit_agent_start(run_id_str, node_name)
                        await publish_pipeline_event(
                            run_id_str, "agent:start", {"agent_name": node_name}
                        )

                    elif kind == "on_chat_model_stream":
                        chunk = event.get("data", {}).get("chunk")
                        token = ""
                        if chunk is not None:
                            token = getattr(chunk, "content", "") or ""
                        if token:
                            agent = get_agent_name_from_active(active_nodes)
                            await ws.emit_agent_chunk(run_id_str, agent, token)
                            await publish_pipeline_event(
                                run_id_str,
                                "agent:chunk",
                                {"agent_name": agent, "token": token},
                            )

                    elif kind == "on_chain_end" and node_name in GRAPH_NODES:
                        output_key = NODE_OUTPUT_KEYS.get(node_name, node_name)
                        latency = metrics.node_latency_ms(node_name)
                        logger.info(
                            "graph_node_completed",
                            node=node_name,
                            run_id=run_id_str,
                            latency_ms=latency,
                        )
                        await self._flush_node_traces(run.id, metrics, node_name, latency)
                        await ws.emit_agent_done(run_id_str, node_name, output_key)
                        await publish_pipeline_event(
                            run_id_str,
                            "agent:done",
                            {"agent_name": node_name, "output_key": output_key},
                        )
                        active_nodes.discard(node_name)

                snapshot = await graph.aget_state(graph_config)
                state = snapshot.values or {}
                await self._persist_state(run, state)
                await self._persist_published(run, state)

                if snapshot.next:
                    run.status = PipelineStatus.hitl_wait
                    await redis.set(HITL_PENDING.format(run_id=run_id_str), "1", ex=settings.pipeline_state_ttl)
                    drafts = await self._drafts_payload(run.id)
                    await ws.emit_hitl_ready(run_id_str, drafts)
                    await publish_pipeline_event(
                        run_id_str, "hitl:ready", {"run_id": run_id_str, "drafts": drafts}
                    )
                else:
                    run.status = PipelineStatus.done
                    run.completed_at = datetime.now(UTC)
                    await redis.delete(HITL_PENDING.format(run_id=run_id_str))

                await apply_run_metrics(self.db, run, metrics)
                recorder.record_eval("pipeline.completed", run.status.value, total_tokens=run.total_tokens)
                await publish_pipeline_event(
                    run_id_str,
                    "pipeline:status",
                    {"status": run.status.value, "total_tokens": run.total_tokens},
                )

        except asyncio.CancelledError:
            run.status = PipelineStatus.error
            run.state_snapshot = {**(run.state_snapshot or {}), "error": "Cancelled"}
            run.completed_at = datetime.now(UTC)
            await ws.emit_pipeline_error(run_id_str, "Cancelled by user")
            await publish_pipeline_event(
                run_id_str, "pipeline:error", {"run_id": run_id_str, "error_msg": "Cancelled"}
            )
        except Exception as exc:
            run.status = PipelineStatus.error
            run.state_snapshot = {**(run.state_snapshot or {}), "error": str(exc)}
            run.completed_at = datetime.now(UTC)
            await ws.emit_pipeline_error(run_id_str, str(exc))
            await publish_pipeline_event(
                run_id_str, "pipeline:error", {"run_id": run_id_str, "error_msg": str(exc)}
            )
        finally:
            export_trace_summary(recorder, trace_name="content_factory.pipeline")
            set_recorder(None)
            clear_trace_context()
            unregister_run_metrics(run_id_str)
            await redis.delete(PIPELINE_STATE.format(run_id=run_id_str))
            from app.core.cancel_registry import clear_cancelled, unregister_task

            unregister_task(run_id_str)
            clear_cancelled(run_id_str)
            await self.db.flush()

    async def resume_after_hitl(
        self,
        run: PipelineRun,
        hitl_approved: dict,
        hitl_edits: dict,
    ) -> PipelineRun:
        redis = get_redis()
        await redis.delete(HITL_PENDING.format(run_id=str(run.id)))
        await self.execute_run(
            run.id,
            resume=True,
            hitl_approved=hitl_approved,
            hitl_edits=hitl_edits,
        )
        await self.db.refresh(run)
        return run

    async def cancel_run(self, run: PipelineRun) -> None:
        run_id_str = str(run.id)
        mark_cancelled(run_id_str)
        run.status = PipelineStatus.error
        run.state_snapshot = {**(run.state_snapshot or {}), "error": "Cancelled by user"}
        run.completed_at = datetime.now(UTC)
        redis = get_redis()
        await redis.delete(PIPELINE_STATE.format(run_id=run_id_str))
        await redis.delete(HITL_PENDING.format(run_id=run_id_str))
        await ws.emit_pipeline_error(run_id_str, "Cancelled by user")
        await publish_pipeline_event(
            run_id_str, "pipeline:error", {"run_id": run_id_str, "error_msg": "Cancelled by user"}
        )
        await self.db.flush()

    async def _flush_node_traces(
        self,
        run_id: uuid.UUID,
        metrics: RunMetrics,
        node_name: str,
        latency_ms: int,
    ) -> None:
        if node_name == "enrich":
            target_agents = ["visual", "seo"]
        else:
            target_agents = [node_name]

        matched = [c for c in metrics.llm_calls if c.get("agent") in target_agents]
        if matched:
            for call in matched:
                await record_agent_trace(
                    self.db,
                    run_id,
                    call.get("agent") or node_name,
                    model_used=call.get("model"),
                    input_tokens=call.get("input_tokens", 0),
                    output_tokens=call.get("output_tokens", 0),
                    latency_ms=call.get("latency_ms", latency_ms),
                    langfuse_trace_id=call.get("langfuse_trace_id"),
                )
            metrics.llm_calls = [c for c in metrics.llm_calls if c not in matched]
        elif node_name in ("hitl", "publish"):
            await record_agent_trace(
                self.db,
                run_id,
                node_name,
                model_used="n/a",
                input_tokens=0,
                output_tokens=0,
                latency_ms=latency_ms,
            )

    async def _drafts_payload(self, run_id: uuid.UUID) -> list[dict]:
        result = await self.db.execute(select(ContentDraft).where(ContentDraft.run_id == run_id))
        return [
            {
                "id": str(d.id),
                "platform": d.platform.value,
                "draft_content": d.draft_content,
                "edited_content": d.edited_content,
                "seo_keywords": d.seo_keywords,
                "hashtags": d.hashtags,
                "hook_variant": d.hook_variant,
                "char_count": d.char_count,
            }
            for d in result.scalars().all()
        ]

    async def _persist_state(self, run: PipelineRun, state: dict) -> None:
        run.state_snapshot = state
        drafts = state.get("platform_drafts") or {}
        seo = state.get("seo_data") or {}

        for platform_name, draft_data in drafts.items():
            try:
                platform = Platform(platform_name)
            except ValueError:
                continue

            content = draft_data.get("content", "") if isinstance(draft_data, dict) else str(draft_data)
            existing = await self.db.execute(
                select(ContentDraft).where(
                    ContentDraft.run_id == run.id,
                    ContentDraft.platform == platform,
                )
            )
            draft = existing.scalar_one_or_none()
            if draft:
                draft.draft_content = content
                draft.hook_variant = draft_data.get("hook") if isinstance(draft_data, dict) else None
                draft.char_count = len(content)
                draft.seo_keywords = seo.get("keywords")
                draft.hashtags = seo.get("hashtags")
            else:
                self.db.add(
                    ContentDraft(
                        run_id=run.id,
                        platform=platform,
                        draft_content=content,
                        hook_variant=draft_data.get("hook") if isinstance(draft_data, dict) else None,
                        char_count=len(content),
                        seo_keywords=seo.get("keywords"),
                        hashtags=seo.get("hashtags"),
                    )
                )

    async def _persist_published(self, run: PipelineRun, state: dict) -> None:
        published = state.get("published_results") or {}
        if not published:
            return

        publisher = PublisherService()
        redis = get_redis()
        run_id_str = str(run.id)
        snap = run.state_snapshot or {}
        gateway_case_id = snap.get("config", {}).get("gateway_case_id") or f"pipeline-{run_id_str}"

        user_tokens: dict = {}
        result = await self.db.execute(select(User).where(User.id == run.user_id))
        user = result.scalar_one_or_none()
        if user and user.platform_tokens:
            user_tokens = user.platform_tokens

        for platform_name, result_data in published.items():
            try:
                platform = Platform(platform_name)
            except ValueError:
                continue

            draft_result = await self.db.execute(
                select(ContentDraft).where(
                    ContentDraft.run_id == run.id,
                    ContentDraft.platform == platform,
                )
            )
            draft = draft_result.scalar_one_or_none()
            if not draft:
                continue

            existing = await self.db.execute(
                select(PublishedPost).where(PublishedPost.draft_id == draft.id)
            )
            if existing.scalar_one_or_none():
                continue

            token_data = user_tokens.get(platform_name) or {}
            access_token = ""
            if isinstance(token_data, dict):
                access_token = str(token_data.get("access_token") or "")

            try:
                post = await publisher.publish_draft(
                    draft,
                    access_token=access_token,
                    case_id=f"{gateway_case_id}-{platform_name}",
                    skip_gateway=settings.aegisai_gateway_fail_open and not settings.aegisai_api_base_url,
                )
            except Exception as exc:
                logger.warning("Publish blocked or failed for %s: %s", platform_name, exc)
                continue

            self.db.add(post)

            post_id = post.external_post_id or ""
            post_url = post.post_url or ""

            await ws.emit_publish_result(run_id_str, platform_name, post_id, post_url)
            await publish_pipeline_event(
                run_id_str,
                "publish:result",
                {"platform": platform_name, "post_id": post_id, "url": post_url},
            )

            # Enqueue Celery publish job (queue:publish stream key for observability)
            await redis.xadd(
                PUBLISH_QUEUE,
                {"draft_id": str(draft.id), "platform": platform_name, "run_id": str(run.id)},
            )
            try:
                from app.worker import publish_to_platform

                publish_to_platform.delay(str(draft.id), platform_name, "")
            except Exception:
                pass


def get_agent_name_from_active(active: set[str]) -> str:
    if not active:
        return "agent"
    # Prefer enrich child agents if in enrich phase
    for name in ("content", "research", "enrich", "publish", "hitl"):
        if name in active:
            return name
    return next(iter(active))


async def _execute_pipeline_background(run_id: uuid.UUID) -> None:
    from app.core.cancel_registry import register_task, unregister_task

    task = asyncio.current_task()
    if task:
        register_task(str(run_id), task)

    try:
        async with async_session_factory() as db:
            result = await db.execute(select(PipelineRun).where(PipelineRun.id == run_id))
            run = result.scalar_one_or_none()
            if not run:
                logger.warning("Pipeline run %s not found", run_id)
                return
            snap = run.state_snapshot or {}
            service = PipelineService(db)
            await service.execute_run(
                run_id,
                platforms=snap.get("platforms"),
                config=snap.get("config"),
            )
            await db.commit()
    except Exception as exc:
        logger.exception("Pipeline %s background execution failed", run_id)
        try:
            async with async_session_factory() as db:
                result = await db.execute(select(PipelineRun).where(PipelineRun.id == run_id))
                run = result.scalar_one_or_none()
                if run and run.status == PipelineStatus.running:
                    run.status = PipelineStatus.error
                    run.state_snapshot = {**(run.state_snapshot or {}), "error": str(exc)}
                    run.completed_at = datetime.now(UTC)
                    await db.commit()
        except Exception:
            logger.exception("Failed to persist error for pipeline %s", run_id)
    finally:
        unregister_task(str(run_id))
