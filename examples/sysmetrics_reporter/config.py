from dataclasses import dataclass
import os
import logging
from uuid import UUID
from typing import Optional


@dataclass
class Config:
    """
    Configuration for the sysmetrics_reporter example.
    """

    report_interval: int = 10  # seconds
    verbose: bool = False
    websuckit_api_key: Optional[str] = os.getenv("WEBSUCKIT_API_KEY")
    websuckit_user_id: Optional[UUID] = UUID(os.getenv("WEB_SUCKIT_USER_ID"))
    websuckit_public_key: Optional[str] = os.getenv("WEB_SUCKIT_PUBLIC_KEY")
    websuckit_channel_pass_key: Optional[str] = os.getenv("WEBSUCKIT_CHANNEL_PASS_KEY")
    websuckit_channel_id: Optional[UUID] = UUID(os.getenv("WEBSUCKIT_CHANNEL_ID"))
    websuckit_channel_name: str = "SysmetricsReporter"


logging.basicConfig(level=logging.INFO if not Config.verbose else logging.WARNING)
