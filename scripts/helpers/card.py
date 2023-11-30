from uuid import UUID
from typing import List
from datetime import datetime
import json_fix
import sys


class Card:
    id: str
    phase: int | None
    question: str
    answers: [str]
    is_open_question: bool
    base64_encoded_image: str | None
    correctly_answered_counter: int | None
    total_answered_counter: int | None
    due_after_date: datetime | None

    def __json__(self):
        result = self.__dict__
        return result

    def __init__(self, question: str, answers: List[str], is_open_question: bool, phase: int | None = None,  base64_encoded_image: str | None = None, correctly_answered_counter: int | None = None, total_answered_counter: int | None = None,
                 due_after_date: datetime | None = None
                 ) -> None:
        # Hash question and answers to generate id
        hashValue = hash(tuple([tuple([a.strip() for a in answers]),
                                question, base64_encoded_image, is_open_question]))

        self.id = (hashValue if hashValue > 0 else -1*hashValue).__str__()
        self.phase = phase
        self.question = question.strip()
        self.answers = [a.strip() for a in answers]
        self.is_open_question = is_open_question
        self.base64_encoded_image = base64_encoded_image
        self.correctly_answered_counter = correctly_answered_counter
        self.total_answered_counter = total_answered_counter
        self.due_after_date = due_after_date
