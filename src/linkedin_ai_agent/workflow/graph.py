from uuid import uuid4

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from linkedin_ai_agent.workflow.state import PostState


def research_node(state: PostState) -> dict:
    """Simulate the research phase."""

    return {
        "research_results": [
            {
                "title": "Example AI news",
                "url": "https://example.com/ai-news",
                "source": "Example source",
            }
        ]
    }


def ranking_node(state: PostState) -> dict:
    """Simulate the story ranking phase."""

    if not state["research_results"]:
        return {
            "selected_story_id": None,
        }

    return {
        "selected_story_id": uuid4(),
    }


def writer_node(state: PostState) -> dict:
    """Simulate content generation."""

    if state["selected_story_id"] is None:
        return {
            "draft": None,
        }

    return {
        "draft": (
            "Este é um post de exemplo gerado pelo workflow. "
            "Em breve, esta etapa utilizará um modelo de linguagem."
        )
    }


def reviewer_node(state: PostState) -> dict:
    """Simulate the content review phase."""

    if state["draft"] is None:
        return {
            "review": {
                "approved": False,
                "reason": "No draft avaliable.",
            }
        }

    return {
        "review": {
            "approved": True,
            "reason": "Draft passed the simulated review.",
        }
    }


def build_graph():
    """Build and compile the post creation workflow."""

    workflow = StateGraph(PostState)

    workflow.add_node("research", research_node)
    workflow.add_node("ranking", ranking_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("publisher", publisher_node)

    workflow.add_edge(START, "research")
    workflow.add_edge("research", "ranking")
    workflow.add_edge("ranking", "writer")
    workflow.add_edge("writer", "reviewer")
    workflow.add_edge("reviewer", "human_approval")

    workflow.add_conditional_edges(
        "human_approval",
        approval_router,
        {
            "publisher": "publisher",
            "end": END,
        },
    )

    workflow.add_edge("publisher", END)

    checkpointer = InMemorySaver()

    return workflow.compile(
        checkpointer=checkpointer,
    )


def human_approval_node(state: PostState) -> dict:
    """Pause the workflow and request human approval."""

    decision = interrupt(
        {
            "type": "content_approval",
            "question": "Do you approve this post for publication?",
            "draft": state["draft"],
        }
    )
    return {
        "approval": decision,
    }


def publisher_node(state: PostState) -> dict:
    """Simulate publication."""

    return {
        "publication": {
            "published": True,
            "platform": "linkedin",
        }
    }


def approval_router(state: PostState) -> str:
    """Route the workflow according to human approval."""

    approval = state["approval"]

    if approval is None:
        return "end"

    if approval.get("approved") is True:
        return "publisher"

    return "end"
