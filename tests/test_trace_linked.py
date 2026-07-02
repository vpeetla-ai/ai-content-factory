"""Trace-linked observability tests."""

from app.vpeetla_observability.context import bind_trace_context, clear_trace_context, get_root_trace_id
from app.vpeetla_observability.recorder import TraceRecorder, get_recorder, set_recorder
from app.vpeetla_observability.spans import eval_score, node_span, system_span


def test_trace_context_propagation():
    bind_trace_context(run_id="run-1", trace_id="trace-1", root_trace_id="trace-1")
    assert get_root_trace_id() == "trace-1"
    clear_trace_context()


def test_recorder_collects_eval_scores():
    recorder = TraceRecorder.create(run_id="run-2", trace_id="trace-2")
    set_recorder(recorder)
    with node_span("research", topic="agents"):
        with eval_score("groundedness", 0.92, source_count=3):
            pass
    assert recorder.eval_scores["groundedness"] == 0.92
    assert any(e.name == "research" for e in recorder.events)
    set_recorder(None)


def test_system_span_records_event():
    recorder = TraceRecorder.create(run_id="run-3", trace_id="trace-3")
    set_recorder(recorder)
    with system_span("pipeline.execute", resume=False):
        pass
    assert any(e.level == "system" for e in recorder.events)
    set_recorder(None)


def test_get_recorder_from_context():
    recorder = TraceRecorder.create(run_id="run-4")
    set_recorder(recorder)
    assert get_recorder() is recorder
    set_recorder(None)
