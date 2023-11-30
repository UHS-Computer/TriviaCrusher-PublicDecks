from uuid import UUID
from typing import List
from datetime import datetime
from helpers.card import Card

from helpers.icon import Icon
import json_fix


class Deck:
    id: str
    name: str
    description: str
    icon: Icon
    cards: [Card]

    def __json__(self):
        result = self.__dict__
        return result

    def __init__(self, id: UUID, name: str, description: str, icon: Icon, cards: [Card]) -> None:
        self.id = id.__str__()
        self.name = name
        self.icon = icon
        self.cards = cards
        self.description = description

    def __markdown__(self) -> str:
        result = ""

        result += "# " + self.name + "\n"
        result += "\n"
        result += "\n"
        result += "## Description\n"
        result += "\n"
        result += self.description + "\n"
        result += "\n"
        result += "\n"
        result += "## Cards\n"
        result += "\n"

        counter = 1
        for card in self.cards:
            result += "### {}. Card\n".format(counter)
            counter += 1
            result += "\n"
            if card.base64_encoded_image is not None:
                imageStringMd = '<p><img src="data:image/jpeg;base64,' + \
                    card.base64_encoded_image + '"></p>'
                result += "{}".format(imageStringMd)

            result += "|Attribut|Value|\n"
            result += "|---|---|\n"
            result += "|Id|{}|\n".format(card.id)
            result += "|Question|{}|\n".format(
                card.question.replace("\n", "\t"))

            if card.is_open_question == True:
                result += "|Answer|{}|\n".format(
                    card.answers[0].replace("\n", "\t"))
            else:
                result += "|Correct Answer|{}|\n".format(
                    card.answers[0].replace("\n", "\t"))

                wrongAnswerCounter = 1
                for wrongAnswer in card.answers[1:]:
                    result += "|Wrong Answer {}|{}|\n".format(
                        wrongAnswerCounter, wrongAnswer.replace("\n", "\t"))
                    wrongAnswerCounter += 1

            result += "\n"
            result += "\n"
        result += "\n"
        result += "## Internal Id"
        result += "\n"
        result += self.id

        return result

    def addOpenQuestion(self, question: str, answer: str, base64_encoded_image: str | None = None) -> None:
        self.cards.append(Card(answers=[
                          answer], question=question, is_open_question=True, base64_encoded_image=base64_encoded_image))
