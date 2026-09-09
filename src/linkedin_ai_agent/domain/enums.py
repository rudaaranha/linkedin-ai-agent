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


class VisualStrategy(str, Enum):
    PERSONAL_ONLY = "personal_only"
    AI_ONLY = "ai_only"
    PERSONAL_AND_AI = "personal_and_ai"


class AuditAction(str, Enum):
    USER_CREATED = "user_created"
    PROFILE_UPDATED = "profile_updated"
    SETTINGS_UPDATED = "settings_updated"

    AI_PROVIDER_CHANGED = "ai_provider_changed"

    CREDENTIAL_CREATED = "credential_created"
    CREDENTIAL_UPDATED = "credential_updated"
    CREDENTIAL_DELETED = "credential_deleted"

    PERSONAL_IMAGE_ADDED = "personal_image_added"
    PERSONAL_IMAGE_DELETED = "personal_image_deleted"

    CONTENT_CREATED = "content_created"
    CONTENT_APPROVED = "content_approved"
    CONTENT_REJECTED = "content_rejected"
    CONTENT_PUBLISHED = "content_published"
