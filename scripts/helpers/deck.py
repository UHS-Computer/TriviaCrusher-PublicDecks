from uuid import UUID
from typing import List
from datetime import datetime
from helpers.card import Card

from helpers.icon import Icon


class Deck:
    id: UUID
    name: str
    icon: Icon
    cards: List[Card]

    def __init__(self, id: UUID, name: str, icon: Icon, cards: List[Card]) -> None:
        self.id = id
        self.name = name
        self.icon = icon
        self.cards = cards

    def addOpenQuestion(self, question: str, answer: str, id: UUID, base64_encoded_image: str | None = None) -> None:
        self.cards.append(Card(id=id, answers=[
                          answer], question=question, is_open_question=True, base64_encoded_image=base64_encoded_image))
