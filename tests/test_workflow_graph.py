from uuid import uuid4

from linkedin_ai_agent.domain.enums import ContentType
from linkedin_ai_agent.workflow.graph import build_graph


def make_initial_state():
    return {
        "user_id": uuid4(),
        "run_id": uuid4(),
        "content_type": ContentType.NEWS,
        "topic": "Artificial Intelligence",
        "research_results": [],
        "selected_story_id": None,
        "draft": None,
        "review": None,
        "visual_strategy": None,
        "selected_image_id": None,
        "generated_image": None,
        "approval": None,
        "publication": None,
    }


def test_graph_executes_successfully():
    graph = build_graph()

    initial_state = make_initial_state()

    result = graph.invoke(initial_state)

    assert result["research_results"]
    assert result["selected_story_id"] is not None
    assert result["draft"] is not None
    assert result["review"] is not None


def test_graph_produces_approved_review_for_valid_draft():
    graph = build_graph()

    result = graph.invoke(make_initial_state())

    assert result["review"]["approved"] is True
