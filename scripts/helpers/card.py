from uuid import UUID
from typing import List
from datetime import datetime
import json_fix
import sys
import hashlib


class Card:
    id: str
    phase: int | None
    question: str
    answers: [str]
    isOpenQuestion: bool
    base64EncodedImage: str | None
    correctlyAnsweredCounter: int | None
    totalAnsweredCounter: int | None
    dueAfterDate: datetime | None

    def __json__(self):
        result = self.__dict__
        return result

    def __init__(self, question: str, answers: List[str], isOpenQuestion: bool, phase: int | None = None,  base64EncodedImage: str | None = None, correctly_answered_counter: int | None = None, total_answered_counter: int | None = None,
                 due_after_date: datetime | None = None
                 ) -> None:
        # Hash question and answers to generate id
        md5 = hashlib.md5(tuple([tuple([a.strip() for a in answers]),
                                question, isOpenQuestion]).__str__().encode()).hexdigest()  # returns a str

        self.id = md5
        self.phase = phase
        self.question = question.strip()
        self.answers = [a.strip() for a in answers]
        self.isOpenQuestion = isOpenQuestion
        self.base64EncodedImage = base64EncodedImage
        self.correctlyAnsweredCounter = correctly_answered_counter
        self.totalAnsweredCounter = total_answered_counter
        self.dueAfterDate = due_after_date
