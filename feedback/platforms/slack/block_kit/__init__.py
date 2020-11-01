from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

__all__ = ("BaseBlock", "BaseElement", "BlockType", "ElementType", "Text", "Option")


class BlockType(Enum):
    ACTIONS = "actions"
    CONTEXT = "context"
    DIVIDER = "divider"
    FILE = "file"
    HEADER = "header"
    IMAGE = "image"
    INPUT = "input"
    SECTION = "section"


class ElementType(Enum):
    BUTTON = "button"
    CHECKBOXES = "checkboxes"
    MULTI_USERS_SELECT = "multi_users_select"
    PLAIN_TEXT_INPUT = "plain_text_input"
    USERS_SELECT = "users_select"


class BaseBlock:
    type: BlockType
    block_id: Optional[str] = None


class BaseElement:
    block_types: List[BlockType]
    type: ElementType


@dataclass
class Text:
    class Type:
        PLAIN = "plain_text"
        MARKDOWN = "mrkdwn"

    type: Type
    text: str  # NOSONAR


@dataclass
class Option:
    text: Text
    value: str
    description: Optional[Text] = None
