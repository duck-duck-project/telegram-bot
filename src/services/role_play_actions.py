from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Self

from aiogram.types import Message

from models import RolePlayAction

__all__ = ('RolePlayActions', 'TrieNode')


@dataclass(slots=True)
class TrieNode:
    children: dict[str, Self] = field(default_factory=dict)
    role_play_action: RolePlayAction | None = None


class RolePlayActions:
    """
    A class to store and search for role play actions by triggers.

    It uses a trie data structure to store triggers and actions
    for more efficient search.
    """

    def __init__(self, role_play_actions: Iterable[RolePlayAction]):
        self.root = TrieNode()
        self.__init_trie(role_play_actions)

    def __init_trie(self, role_play_actions: Iterable[RolePlayAction]):
        self.root = TrieNode()
        for action in role_play_actions:
            for trigger in action.triggers:
                self.__insert(trigger.lower(), action)

    def __insert(self, word, action):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.role_play_action = action

    def __search(self, word) -> RolePlayAction | None:
        node = self.root
        for char in word:
            if char not in node.children:
                return
            node = node.children[char]
        return node.role_play_action

    def get_action(self, message: Message) -> RolePlayAction | None:
        message_text = message.text.lower()
        return self.__search(message_text)
