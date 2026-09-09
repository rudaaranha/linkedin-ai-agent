from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from .enums import (
    AuditAction,
    ContentStatus,
    ContentType,
    DifficultyLevel,
    VisualStrategy,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Profile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    display_name: str
    professional_title: str | None = None
    bio: str | None = None
    expertise: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class UserSettings(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    posts_per_week: int = Field(default=2, ge=1, le=7)
    preferred_post_days: list[int] = Field(default_factory=list)
    preferred_post_time: str | None = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ContentPreferences(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    content_types: list[ContentType] = Field(
        default_factory=lambda: [
            ContentType.NEWS,
            ContentType.EDUCATIONAL,
            ContentType.OPINION,
        ]
    )

    language: str = "pt-BR"
    tone: str = "professional"
    target_audience: str | None = None

    preferred_topics: list[str] = Field(default_factory=list)
    avoided_topics: list[str] = Field(default_factory=list)

    visual_strategy: VisualStrategy = VisualStrategy.AI_ONLY

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class AIConfiguration(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    default_provider: str
    default_model: str

    fallback_provider: str | None = None
    fallback_model: str | None = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ProviderCredential(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    provider: str
    credential_type: str

    # Reference to the secure secret storage.
    # The actual secret must NOT live in the domain model.
    secret_ref: str

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class PersonalImage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    storage_key: str
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    context: str | None = None

    usage_count: int = Field(default=0, ge=0)
    last_used_at: datetime | None = None

    is_active: bool = True

    created_at: datetime = Field(default_factory=utc_now)


class PrivacyProfile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    allow_personal_images: bool = False
    allow_ai_processing: bool = True
    allow_external_ai_providers: bool = True
    allow_analytics: bool = False

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class AuditEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    action: AuditAction
    resource_type: str
    resource_id: UUID | None = None

    metadata: dict[str, str] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=utc_now)


class Topic(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    category: str
    description: str
    difficulty: DifficultyLevel | None = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)


class Article(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    story_id: UUID | None = None

    title: str
    url: HttpUrl
    source: str
    author: str | None = None
    content: str | None = None
    published_at: datetime | None = None
    discovered_at: datetime = Field(default_factory=utc_now)


class Story(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    title: str
    summary: str
    topic_id: UUID | None = None

    relevance_score: float | None = None
    recency_score: float | None = None
    source_quality_score: float | None = None

    is_published: bool = False

    created_at: datetime = Field(default_factory=utc_now)


class Content(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    type: ContentType
    status: ContentStatus = ContentStatus.DISCOVERED

    title: str
    body: str

    topic_id: UUID | None = None
    story_id: UUID | None = None
    difficulty: DifficultyLevel | None = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ContentQueueItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    user_id: UUID
    content_id: UUID

    priority: float = 0.0
    scheduled_date: datetime | None = None

    created_at: datetime = Field(default_factory=utc_now)


class PostHistory(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    user_id: UUID
    content_id: UUID

    content_type: ContentType
    topic_id: UUID | None = None
    story_id: UUID | None = None

    published_at: datetime

    linkedin_post_id: str | None = None
    linkedin_url: HttpUrl | None = None

    impressions: int | None = None
    likes: int | None = None
    comments: int | None = None
    shares: int | None = None


class ResearchRun(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    user_id: UUID

    started_at: datetime
    finished_at: datetime | None = None

    query: str

    sources_searched: int = 0
    articles_found: int = 0
    articles_dicarded: int = 0
    stories_selected: int = 0
