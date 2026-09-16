from uuid import uuid4

from langgraph.graph import END, START, StateGraph

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

    workflow.add_edge(START, "research")
    workflow.add_edge("research", "ranking")
    workflow.add_edge("ranking", "writer")
    workflow.add_edge("writer", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()
