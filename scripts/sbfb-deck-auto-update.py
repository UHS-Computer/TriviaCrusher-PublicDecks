from bs4 import BeautifulSoup
from helpers.icon import Icon
from helpers.deck import Deck
import urllib3
import uuid
import os
from typing import List
import base64
import json

from PIL import Image
from PIL import GifImagePlugin

from helpers.imageConverters import gif2jpg
from helpers.utils import download_image

path_to_tcjson_file = "./de_DE/categories/freizeit/sbfb/sbfb-deck.tcjson"
path_to_md_file = "./de_DE/categories/freizeit/sbfb/sbfb-deck.md"
path_for_images = "./de_DE/categories/freizeit/sbfb/images"

# the deck SBFB consists of of 5 parts which are combined into one big deck here!
urls_to_scan = [
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-Binnen/Basisfragen/Basisfragen-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-Binnen/Spezifische-Fragen-Binnen/Spezifische-Fragen-Binnen-node.html",
]


result = Deck(
    id=uuid.UUID('87eac9dc-ca01-47e0-beea-4210858f5460'),
    name="SBF-Binnen - Sportbootführerschein Binnen Theorie Fragen",
    description="Dies sind die Lernzettel für den Sportbootführerschein Binnen.\nHierzu wurden die offiziellen Prüfungsfragen von <https://www.elwis.de/> in Karteikarten übersetzt.\n\n\nStand des Exports ist: ",
    icon=Icon(
        font_family="MaterialIcons",
        code_point=58701,
        match_text_direction=False,
        font_family_fallback=None,
        font_package=None
    ),
    cards=[]
)

foundStand = False

for url in urls_to_scan:
    resp = urllib3.request("GET", url)
    if resp.status > 250:
        print("Found status code {} while loading sks questions...".format(resp.status))
        exit(1)
    soup = BeautifulSoup(resp.data)

    x = soup.body.find('div', attrs={'id': 'content'})
    paragraphs = (x.findChildren(recursive=False))

    i = 0

    notation_counter = 0

    current_question: str | None = None
    current_answers: List[str] | None = None
    current_base64_image_str: str | None = None
    while i < paragraphs.__len__():
        paragraph = paragraphs[i]

        # Skip headline
        if paragraph.name == "h1":
            i += 1
            continue

        # either a question ends with a '<p class="line"></p>' or with a '<div class="sectionRelated"></div>'
        if (paragraph.attrs.__len__() != 0 and "class" in paragraph.attrs and "line" in paragraph.attrs["class"] and "wsv-red" not in paragraph.attrs["class"]) or (paragraph.name == "div" and paragraph.attrs.__len__() != 0 and "class" in paragraph.attrs and "sectionRelated" in paragraph.attrs["class"]):
            i += 1
            notation_counter = 0

            # complete card
            if current_answers is not None and current_question is not None:
                if current_answers.__len__() != 4:
                    print(
                        "Something went wrong while parsing sbfb questions, as we expect excactly 4 answers for each question...")
                    exit(1)
                result.addClosedQuestion(
                    current_question, current_answers, current_base64_image_str)
                current_question = None
                current_answers = None
                current_base64_image_str = None

            else:
                print("ERROR while parsing site!")
                exit(1)
            continue

        # each question is started with a "Nummer X:" paragraph
        if "Nummer " in paragraph.get_text() and paragraph.get_text().endswith(":"):
            i += 1
            notation_counter = 0

            continue

        # 'Stand: XXXXXXX' determines the latest update for that page!
        if "Stand: " in paragraph.get_text():
            i += 1
            notation_counter = 0

            if foundStand == False:
                result.description += paragraph.get_text()
                foundStand = True
            continue

        # Either we read a question or an answer...
        if notation_counter == 0:
            # interpret the paragraph as question
            notation_counter += 1
            current_question = paragraph.get_text()
            if "Anmerkung:" in current_question or current_question.strip().__len__() == 0:
                notation_counter = 0
                current_question = None
                i += 1
                continue

            if paragraph.find_all("img").__len__() != 0:
                image_paths = []
                for img in paragraph.find_all("img"):
                    image_filename = img.attrs["src"].split(
                        "/")[-1].split("?")[0]

                    file_path_folder = 'images/'
                    file_path = file_path_folder + image_filename

                    download_image(
                        img.attrs["src"], file_path_folder, image_filename)

                    if image_filename.endswith(".gif"):
                        convertedImages = gif2jpg(file_path=file_path_folder, file_name=image_filename, num_key_frames=1,
                                                  trans_color=(255, 255, 255))
                        image_paths += convertedImages
                    else:
                        image_paths.append(file_path)

                # if multiple images, combine them into one image
                if image_paths.__len__() >= 1:
                    # Read the images
                    images = [Image.open(i) for i in image_paths]

                    # find maximum width of images
                    newImageWidth = max([image.size[0] for image in images])
                    newImageHeight = sum([image.size[1] for image in images])
                    new_image = Image.new(
                        'RGB', (newImageWidth, newImageHeight), (250, 250, 250))

                    current_y_offset = 0
                    for image in images:
                        new_image.paste(image, (0, current_y_offset))
                        current_y_offset += image.size[1]

                    cardId = result.cards.__len__()
                    new_image.save(
                        "images/merged_image_{}.jpg".format(cardId), "JPEG")

                    # Convert the image to base64 format
                    with open("images/merged_image_{}.jpg".format(cardId), "rb") as f:
                        # set image base 64 value for card.
                        temp = base64.b64encode(f.read())
                        current_base64_image_str = temp.decode(
                            'utf-8')  # convert bytes to string

        elif notation_counter == 1:
            # interpret the paragraph as answer
            notation_counter += 1
            current_answers = [i.strip() for i in (
                str(paragraph.get_text())).splitlines() if i.strip() and i.strip().replace(".", "")]
            if current_answers == [] or (current_answers.__len__() == 1 and current_answers[0].strip() == ""):
                current_answers = None
                notation_counter -= 1
            if current_answers is not None and current_answers.__len__() == 8 and "279" in current_question:
                new_answers = []
                counter_for_formatting = 0
                for answer in current_answers:
                    if counter_for_formatting == 0:
                        new_answers.append(answer)
                        counter_for_formatting = 1
                    else:
                        new_answers[-1] += answer
                        counter_for_formatting = 0
                current_answers = new_answers

            if current_answers is not None and current_answers.__len__() != 4:
                print("meh")

        elif notation_counter > 1:
            # interpret the paragraph as answer
            notation_counter += 1
            current_answers.append(paragraph.get_text())

        i += 1

f = open(path_to_tcjson_file, 'w')
f.write(json.dumps(result, indent=2))
f.close()

f = open(path_to_md_file, 'w')
f.write(result.__markdown__(path_for_images))
f.close()
