from typing import Any, TypedDict
from uuid import UUID

from linkedin_ai_agent.domain.enums import ContentType


class PostState(TypedDict):
    user_id: UUID
    run_id: UUID

    content_type: ContentType
    topic: str | None

    research_results: list[dict[str, Any]]

    selected_story_id: UUID | None

    draft: str | None

    review: dict[str, Any] | None

    visual_strategy: str | None
    selected_image_id: UUID | None
    generated_image: str | None

    approval: dict[str, Any] | None

    publication: dict[str, Any] | None
