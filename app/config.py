import os
import logging
from typing import Optional, Dict, Any
from pydantic import BaseSettings, validator
from logging.handlers import RotatingFileHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'app.log',
            maxBytes=10485760,  # 10MB
            backupCount=3
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("config")


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

    @validator('TEMPLATE_DIR', 'STATIC_DIR')
    def validate_directory_exists(cls, v):
        """Validate that the specified directory exists."""
        if not os.path.isdir(v):
            logger.warning(f"Directory not found: {v}")
        return v

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
try:
    settings = Settings()
    logger.info("Configuration loaded successfully")

    # Log debug mode
    if settings.DEBUG:
        logger.info("Application running in DEBUG mode")

    # Additional validation
    if not os.path.exists(settings.TEMPLATE_DIR):
        logger.warning(f"Template directory does not exist: {settings.TEMPLATE_DIR}")
    if not os.path.exists(settings.STATIC_DIR):
        logger.warning(f"Static directory does not exist: {settings.STATIC_DIR}")

except Exception as e:
    logger.error(f"Error loading configuration: {str(e)}")
    # Fallback to default settings
    settings = Settings()