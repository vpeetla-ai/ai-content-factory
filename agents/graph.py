"""LangGraph StateGraph — full pipeline per architecture LLD."""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from agents.nodes.content import content_agent
from agents.nodes.enrich import enrich_node
from agents.nodes.hitl import human_review_node
from agents.nodes.publish import publisher_agent
from agents.nodes.research import research_agent
from agents.state import ContentFactoryState


def build_graph(*, checkpointer=None):
  """Build and compile the Content Factory agent graph.

  Flow: research → content → enrich (visual+seo parallel) → hitl → publish → END
  HITL uses interrupt_before on the hitl node.
  """
  builder = StateGraph(ContentFactoryState)

  builder.add_node("research", research_agent)
  builder.add_node("content", content_agent)
  builder.add_node("enrich", enrich_node)
  builder.add_node("hitl", human_review_node)
  builder.add_node("publish", publisher_agent)

  builder.add_edge(START, "research")
  builder.add_edge("research", "content")
  builder.add_edge("content", "enrich")
  builder.add_edge("enrich", "hitl")
  builder.add_edge("hitl", "publish")
  builder.add_edge("publish", END)

  cp = checkpointer or MemorySaver()
  return builder.compile(
      checkpointer=cp,
      interrupt_before=["hitl"],
  )
