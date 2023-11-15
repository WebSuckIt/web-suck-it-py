import logging
import os
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Config:
    """
    Configuration for the sysmetrics_reporter example.
    """

    report_interval: int = 60  # seconds
    verbose: bool = False
    websuckit_user_access_key: Optional[str] = os.getenv("WEBSUCKIT_USER_ACCESS_KEY")
    websuckit_user_id: Optional[UUID] = UUID(os.getenv("WEB_SUCKIT_USER_ID"))
    websuckit_public_key: Optional[str] = os.getenv("WEB_SUCKIT_PUBLIC_KEY")
    websuckit_channel_name: Optional[str] = os.getenv("WEBSUCKIT_CHANNEL_NAME")


logging.basicConfig(level=logging.INFO if not Config.verbose else logging.WARNING)
