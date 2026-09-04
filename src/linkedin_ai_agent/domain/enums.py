from enum import Enum


class ContentType(str, Enum):
    NEWS = "news"
    EDUCATIONAL = "educational"
    OPINION = "opinion"


class ContentStatus(str, Enum):
    DISCOVERED = "discovered"
    RANKED = "ranked"
    QUEUED = "queued"
    DRAFTED = "drafted"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    DISCARDED = "descarded"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
