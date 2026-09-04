from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from .enums import ContentStatus, ContentType, DifficultyLevel


class Topic(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    name: str
    category: str
    description: str

    dificulty: DifficultyLevel | None = None
    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.now)


class Article(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    story_id: UUID | None = None

    title: str
    url: HttpUrl
    source: str

    author: str | None = None
    content: str | None = None

    published_at: datetime | None = None
    discovered_at: datetime | None = None


class Story(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    title: str
    summary: str

    topic_id: UUID | None = None

    relevance_score: float | None = None
    recency_score: float | None = None
    source_quality_score: float | None = None

    is_published: bool = False

    created_at: datetime = Field(default_factory=datetime.now)


class Content(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    type: ContentType
    status: ContentStatus = ContentStatus.DISCOVERED

    title: str
    body: str

    topic_id: UUID | None = None
    story_id: UUID | None = None

    difficulty: DifficultyLevel | None = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ContentQueueItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    content_id: UUID

    priority: float = 0.0
    scheduled_date: datetime | None = None

    created_at: datetime = Field(default_factory=datetime.now)


class PostHistory(BaseModel):
    id: UUID = Field(default_factory=uuid4)

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

    started_at: datetime
    finished_at: datetime | None = None

    query: str

    sources_searched: int = 0
    articles_found: int = 0
    articles_dicarded: int = 0
    stories_selected: int = 0
