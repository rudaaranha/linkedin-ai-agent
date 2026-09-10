from datetime import UTC, datetime, timedelta

from .enums import ContentStatus
from .models import Content, PostHistory, Story


def is_story_already_published(
        story: Story,
        post_history: list[PostHistory],
) -> bool:
    """Return True when the story has already been published"""

    return any(
        post.story_id == story.id
        for post in post_history
        if post.story_id is not None
    )


def can_queue_content(content: Content) -> bool:
    """Return True when content is eligible to enter the publication queue."""

    return content.status in {
        ContentStatus.DISCOVERED,
        ContentStatus.RANKED,
        ContentStatus.DRAFTED,
        ContentStatus.REVIEWED,
    }


def can_publish_content(
        content: Content,
        post_history: list[PostHistory],
        story: Story | None = None,
) -> bool:
    """
    Return True when content satisfies the minumum publication rules.

    Human approval is mandatory before publication
    """

    if content.status != ContentStatus.APPROVED:
        return False

    if any(post.content_id == content.id for post in post_history):
        return False

    if story is not None and is_story_already_published(story, post_history):
        return False

    return True


def meets_news_quality_threshold(
        score: float | None,
        minimum_score: float = 7.0,
) -> bool:
    """Return True when a news score reaches the minumum quality threshold"""

    if score is None:
        return False

    return score >= minimum_score


def should_research(
        queue_size: int,
        queue_target: int,
        last_research_at: datetime | None,
        cooldown_days: int = 14,
        now: datetime | None = None,
) -> bool:
    """
    Return True when the system should perform a new research run.

    Research is needed only when the queue is below its target and 
    the research cooldown has elapsed
    """

    if queue_size >= queue_target:
        return False

    if last_research_at is None:
        return True

    if now is None:
        now = datetime.now(UTC)

    cooldown = timedelta(days=cooldown_days)

    return now - last_research_at >= cooldown
    