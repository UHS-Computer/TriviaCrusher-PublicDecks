from uuid import UUID
from typing import List
from datetime import datetime
from helpers.card import Card

from helpers.icon import Icon
import json_fix


class Deck:
    id: str
    name: str
    icon: Icon
    cards: [Card]

    def __json__(self):
        result = self.__dict__
        return result

    def __init__(self, id: UUID, name: str, icon: Icon, cards: [Card]) -> None:
        self.id = id.__str__()
        self.name = name
        self.icon = icon
        self.cards = cards

    def addOpenQuestion(self, question: str, answer: str, id: UUID, base64_encoded_image: str | None = None) -> None:
        self.cards.append(Card(id=id.__str__(), answers=[
                          answer], question=question, is_open_question=True, base64_encoded_image=base64_encoded_image))
