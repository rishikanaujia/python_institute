import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings.

    These settings can be configured using environment variables or .env file.
    """

    # Application settings
    APP_NAME: str = "Python Institute"
    APP_DESCRIPTION: str = "Professional Python Certification & Training Courses"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Template settings
    TEMPLATE_DIR: str = "app/templates"
    STATIC_DIR: str = "app/static"

    # Contact information
    CONTACT_EMAIL: str = "info@pythoninstitute.org"
    CONTACT_PHONE: str = "+1 (123) 456-7890"
    CONTACT_ADDRESS: str = "1234 Python Way, Coding District, San Francisco, CA 94107"

    # Social media links
    TWITTER_URL: Optional[str] = "https://twitter.com/pythoninstitute"
    FACEBOOK_URL: Optional[str] = "https://facebook.com/pythoninstitute"
    LINKEDIN_URL: Optional[str] = "https://linkedin.com/company/pythoninstitute"
    GITHUB_URL: Optional[str] = "https://github.com/pythoninstitute"
    YOUTUBE_URL: Optional[str] = "https://youtube.com/pythoninstitute"

    # SEO settings
    META_KEYWORDS: str = "Python, certification, programming, training, PCEP, PCAP, PCPP"
    META_AUTHOR: str = "Python Institute"

    # Course information
    COURSE_LEVELS: list = ["Beginner", "Intermediate", "Advanced", "Expert"]

    # Certification types
    CERTIFICATION_TYPES: list = ["PCEP™", "PCAP™", "PCPP1™", "PCPP2™"]

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()