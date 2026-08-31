from linkedin_ai_agent.core.config import settings


def test_settings():
    assert settings.app_name == "LinkedIn AI Agent"
    assert settings.app_env == "development"
    assert settings.deepseek_api_key == "test-deepseek-key"
