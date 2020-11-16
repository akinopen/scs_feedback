from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from feedback.platforms.slack.block_kit import (
    BaseElement,
    BlockType,
    ElementType,
    Option,
    Text,
)

__all__ = ("Button", "Checkboxes", "MultiUsersSelect", "PlainTextInput", "UsersSelect")


@dataclass
class Button(BaseElement):
    class Style(Enum):
        DEFAULT = None
        PRIMARY = "primary"
        DANGER = "danger"

    action_id: str
    text: Text
    block_types = [BlockType.ACTIONS, BlockType.SECTION]
    type: ElementType = ElementType.BUTTON
    url: Optional[str] = None
    value: Optional[str] = None
    style: Optional[Style] = Style.DEFAULT


@dataclass
class Checkboxes(BaseElement):
    action_id: str
    options: List[Option]
    type: ElementType = ElementType.CHECKBOXES


@dataclass
class MultiUsersSelect(BaseElement):
    action_id: str
    placeholder: Text
    type: ElementType = ElementType.MULTI_USERS_SELECT


@dataclass
class PlainTextInput(BaseElement):
    action_id: str
    multiline: bool = False
    placeholder: Optional[str] = None
    type: ElementType = ElementType.PLAIN_TEXT_INPUT


@dataclass
class UsersSelect(BaseElement):
    action_id: str
    placeholder: Text
    type: ElementType = ElementType.USERS_SELECT
