from uuid import UUID
from typing import List
from datetime import datetime


class Card:
    id: UUID
    phase: int | None
    question: str
    answers: List[str]
    is_open_question: bool
    base64_encoded_image: str | None
    correctly_answered_counter: int | None
    total_answered_counter: int | None
    due_after_date: datetime | None

    def __init__(self, id: UUID, question: str, answers: List[str], is_open_question: bool, phase: int | None = None,  base64_encoded_image: str | None = None, correctly_answered_counter: int | None = None, total_answered_counter: int | None = None, due_after_date: datetime | None = None) -> None:
        self.id = id
        self.phase = phase
        self.question = question
        self.answers = answers
        self.is_open_question = is_open_question
        self.base64_encoded_image = base64_encoded_image
        self.correctly_answered_counter = correctly_answered_counter
        self.total_answered_counter = total_answered_counter
        self.due_after_date = due_after_date
