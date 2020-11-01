from dataclasses import dataclass
from typing import Any, List

from feedback.platforms.slack.block_kit import BaseBlock, BaseElement, BlockType, Text

__all__ = ("Actions", "Divider", "Input", "Section")


@dataclass
class Actions(BaseBlock):
    elements: List[Any]
    type: BlockType = BlockType.ACTIONS


@dataclass
class Divider(BaseBlock):
    type: BlockType = BlockType.DIVIDER


@dataclass
class Input(BaseBlock):
    label: Text
    element: BaseElement
    block_id: str
    type: BlockType = BlockType.INPUT


@dataclass
class Section(BaseBlock):
    text: Text
    type: BlockType = BlockType.SECTION
