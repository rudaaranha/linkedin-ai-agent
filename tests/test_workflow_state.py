from uuid import uuid4

from linkedin_ai_agent.domain.enums import ContentType
from linkedin_ai_agent.workflow.state import PostState


def test_post_state_can_be_created():
    user_id = uuid4()
    run_id = uuid4()

    state: PostState = {
        "user_id": user_id,
        "run_id": run_id,
        "content_type": ContentType.NEWS,
        "topic": "LLMs",
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


    assert state["user_id"] == user_id
    assert state["run_id"] == run_id
    assert state["content_type"] == ContentType.NEWS
    assert state["research_results"] == []
    assert state["draft"] is None
