from datetime import UTC, datetime, timedelta
from uuid import uuid4

from linkedin_ai_agent.domain.enums import ContentStatus, ContentType
from linkedin_ai_agent.domain.models import Content, PostHistory, Story
from linkedin_ai_agent.domain.rules import (
    can_publish_content,
    can_queue_content,
    is_story_already_published,
    meets_news_quality_threshold,
    should_research,
)



def make_content(
        status:ContentStatus,
) -> Content:
    return Content(
        user_id=uuid4(),
        type=ContentType.NEWS,
        status=status,
        title="Test content",
        body="Test body",
    )


def make_story() -> Story:
    return Story(
        title="Test story",
        summary="Test summary",
    )


def make_post_history(
        content_id,
        story_id = None,
) -> PostHistory:
    return PostHistory(
        user_id=uuid4(),
        content_id=content_id,
        content_type=ContentType.NEWS,
        story_id=story_id,
        published_at=datetime.now(UTC),
    )


def test_approved_content_can_be_published():
    content = make_content(ContentStatus.APPROVED)

    assert can_publish_content(content, []) is True


def test_non_approved_content_cannot_be_published():
    content = make_content(ContentStatus.REVIEWED)

    assert can_publish_content(content, []) is False


def test_already_published_content_cannot_be_published_again():
    content = make_content(ContentStatus.APPROVED)

    history = [
        make_post_history(content.id),
    ]

    assert can_publish_content(content, history) is False


def test_already_published_story_cannot_be_published_again():
    content = make_content(ContentStatus.APPROVED)
    story = make_story()

    history = [
        make_post_history(
            content_id=uuid4(),
            story_id=story.id,
        ),
    ]

    assert is_story_already_published(story, history) is True
    assert can_publish_content(content, history, story) is False


def test_new_story_can_be_published():
    content = make_content(ContentStatus.APPROVED)
    story = make_story()

    assert can_publish_content(content, [], story) is True


def test_content_can_enter_queue_when_not_finalized():
    assert can_queue_content(
        make_content(ContentStatus.DISCOVERED)
    ) is True

    assert can_queue_content(
        make_content(ContentStatus.RANKED)
    ) is True

    assert can_queue_content(
        make_content(ContentStatus.DRAFTED)
    ) is True

    assert can_queue_content(
        make_content(ContentStatus.REVIEWED)
    ) is True


def test_published_content_cannot_enter_queue():
    content = make_content(ContentStatus.PUBLISHED)

    assert can_queue_content(content) is False


def test_rejected_content_cannot_enter_queue():
    content = make_content(ContentStatus.REJECTED)

    assert can_queue_content(content) is False


def test_news_above_quality_threshold_is_valid():
    assert meets_news_quality_threshold(8.0) is True


def test_news_at_quality_threshold_is_valid():
    assert meets_news_quality_threshold(7.0) is True


def test_news_below_quality_threshold_is_invalid():
    assert meets_news_quality_threshold(6.9) is False


def test_news_without_score_is_valid():
    assert meets_news_quality_threshold(None) is False


def test_research_is_note_needed_when_queue_is_full():
    assert should_research(
        queue_size=4,
        queue_target=4,
        last_research_at=None,
    ) is False


def test_research_is_needed_when_queue_is_below_target_and_never_researched():
    assert should_research(
        queue_size=2,
        queue_target=4,
        last_research_at=None,
    ) is True


def test_research_is_not_needed_during_cooldown():
    now = datetime.now(UTC)

    last_research = now - timedelta(days=7)

    assert should_research(
        queue_size=2,
        queue_target=4,
        last_research_at=last_research,
        cooldown_days=14,
        now=now,
    ) is False


def test_research_is_needed_after_cooldown():
    now = datetime.now(UTC)

    last_research = now - timedelta(days=14)

    assert should_research(
        queue_size=2,
        queue_target=4,
        last_research_at=last_research,
        cooldown_days=14,
        now=now
    ) is True
