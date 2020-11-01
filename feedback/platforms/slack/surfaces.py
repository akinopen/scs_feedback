from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from feedback.platforms.slack.block_kit import BaseBlock, Text

__all__ = ("Modal", "SurfaceType")


class SurfaceType(Enum):
    MESSAGE = "message"
    MODAL = "modal"
    HOME_TAB = "home"


@dataclass
class Modal:
    title: Text
    blocks: List[BaseBlock]
    type: SurfaceType = SurfaceType.MODAL
    submit: Optional[Text] = None
    close: Optional[Text] = None
    callback_id: Optional[str] = None
