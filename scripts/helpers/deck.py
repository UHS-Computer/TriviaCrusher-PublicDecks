from uuid import UUID
from typing import List
from datetime import datetime
from helpers.card import Card
import base64
from PIL import Image
import os
from helpers.icon import Icon
import json_fix
import io


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

    def __markdown__(self, imagePath: str) -> str:
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
        imageCounter = 1
        for card in self.cards:
            result += "### {}. Card\n".format(counter)
            counter += 1
            result += "\n"
            result += "|Attribut|Value|\n"
            result += "|---|---|\n"
            result += "|Id|{}|\n".format(card.id)
            result += "|Question|{}|\n".format(
                card.question.replace("\n", "\t"))

            if card.base64EncodedImage is not None:
                # ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://myoctocat.com/assets/images/base-octocat.svg)
                # imageStringMd = '<img src="data:image/jpeg;base64,' + \
                #     card.base64EncodedImage + '" />'
                fileName = 'test{}.jpeg'.format(imageCounter)
                imageStringMd = '![Question Image {}]({})'.format(
                    imageCounter, "./images/" + fileName)
                imageCounter += 1
                result += "|Image|{}|\n".format(imageStringMd)

                image = base64.b64decode(str(card.base64EncodedImage))
                imagePathAndFilename = (imagePath + "/" + fileName)
                isExist = os.path.exists(imagePath)
                if not isExist:
                    # Create a new directory because it does not exist
                    os.makedirs(imagePath)

                img = Image.open(io.BytesIO(image))
                img.save(imagePathAndFilename, 'jpeg')

            if card.isOpenQuestion == True:
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

    def addOpenQuestion(self, question: str, answer: str, base64EncodedImage: str | None = None) -> None:
        self.cards.append(Card(answers=[
                          answer], question=question, isOpenQuestion=True, base64EncodedImage=base64EncodedImage))
