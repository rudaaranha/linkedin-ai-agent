from typing import Any, TypedDict
from uuid import UUID

from linkedin_ai_agent.domain.enums import ApprovalDecision, ContentType


class HumanApproval(TypedDict):
    decision: ApprovalDecision
    feedback: str | None


class PostState(TypedDict):
    user_id: UUID
    run_id: UUID

    content_type: ContentType
    topic: str | None

    research_results: list[dict[str, Any]]

    selected_story_id: UUID | None

    draft: str | None

    revision_feedback: str | None
    regeneration_count: int

    review: dict[str, Any] | None

    visual_strategy: str | None
    selected_image_id: UUID | None
    generated_image: str | None

    approval: HumanApproval | None

    publication: dict[str, Any] | None
