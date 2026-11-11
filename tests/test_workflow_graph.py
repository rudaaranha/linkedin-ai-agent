from uuid import uuid4

from langgraph.types import Command

from linkedin_ai_agent.domain.enums import ContentType
from linkedin_ai_agent.workflow.graph import approval_router, build_graph


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

    config = {
        "configurable": {
            "thread_id": "test-graph-execution",
        }
    }

    result = graph.invoke(
        make_initial_state(),
        config=config,
    )

    assert result["research_results"]
    assert result["selected_story_id"] is not None
    assert result["draft"] is not None
    assert result["review"] is not None
    assert result["__interrupt__"]


def test_graph_produces_approved_review_for_valid_draft():
    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "test-graph-review",
        }
    }

    result = graph.invoke(
        make_initial_state(),
        config=config,
    )

    assert result["review"]["approved"] is True
    assert result["approval"] is None


def test_graph_pauses_for_human_approval():
    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "test-human-approval",
        }
    }

    result = graph.invoke(
        make_initial_state(),
        config=config,
    )

    assert result["approval"] is None
    assert result["publication"] is None
    assert result["__interrupt__"]


def test_graph_publishes_after_human_approval():
    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "test-human-approval-resume",
        }
    }

    # First execution: the workflow pauses.
    paused_result = graph.invoke(
        make_initial_state(),
        config=config,
    )

    assert paused_result["__interrupt__"]

    # Second execution: resume with human approval.
    result = graph.invoke(
        Command(
            resume={
                "approved": True,
                "reason": "Approved by user"
            }
        ),
        config=config,
    )

    assert result["approval"]["approved"] is True
    assert result["publication"]["published"] is True


def test_approval_router_sends_approved_content_to_publisher():
    state = make_initial_state()

    state["approval"] = {
        "approved": True,
    }

    assert approval_router(state) == "publisher"


def test_approval_router_sends_rejected_content_back_to_end():
    state = make_initial_state()

    state["approval"] = {
        "approved": False,
    }

    assert approval_router(state) == "end"


def test_graph_does_not_publish_after_human_rejection():
    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "test-human-rejection",
        }
    }

    paused_result = graph.invoke(
        make_initial_state(),
        config=config,
    )

    assert paused_result["__interrupt__"]

    result = graph.invoke(
        Command(
            resume={
                "approved": False,
                "reason": "Content rejected by user.",
            }
        ),
        config=config,
    )

    assert result["approval"]["approved"] is False
    assert result["publication"] is None
