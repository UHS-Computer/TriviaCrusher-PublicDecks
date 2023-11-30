from bs4 import BeautifulSoup
from helpers.icon import Icon
from helpers.deck import Deck
import urllib3
import uuid


def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib3.urlretrieve(url, full_path)


path_to_tcjson_file = "../de_DE/categories/freizeit/sks/sks-deck.tcjson"

# the deck SKS consists of of 5 parts which are combined into one big deck here!
urls_to_scan = [
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Schifffahrtsrecht/Schifffahrtsrecht-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Navigation/Navigation-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Wetterkunde/Wetterkunde-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Seemannschaft-I/Seemannschaft-I-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Seemannschaft-II/Seemannschaft-II-node.html",
]

result = Deck(
    id=uuid.UUID('8f2274f7-889b-4874-aac7-92a6dc0ef16d'),
    name="SKS - Sportküstenschifferschein Theorie Fragen",
    icon=Icon(
        font_family="MaterialIcons",
        code_point=58701,
        match_text_direction=False,
        font_family_fallback=None,
        font_package=None
    ),
    cards=[]
)


for url in urls_to_scan:
    resp = urllib3.request("GET", url)
    print(resp.status)
    soup = BeautifulSoup(resp.data)

    x = soup.body.find('div', attrs={'id': 'content'})
    # print(x.prettify())
    paragraphs = (x.findChildren(recursive=False))

    i = 0

    notation_counter = 0

    current_question: str | None = None
    current_answer: str | None = None
    while i < paragraphs.__len__():
        paragraph = paragraphs[i]

        # Skip headline
        if paragraph.name == "h1":
            i += 1
            continue

        # either a question ends with a '<p class="line"></p>' or with a '<div class="sectionRelated"></div>'
        if (paragraph.attrs.__len__() != 0 and "class" in paragraph.attrs and "line" in paragraph.attrs["class"]) or (paragraph.name == "div" and paragraph.attrs.__len__() != 0 and "class" in paragraph.attrs and "sectionRelated" in paragraph.attrs["class"]):
            i += 1
            notation_counter = 0

            # complete card
            if current_answer is not None and current_question is not None:
                result.addOpenQuestion(
                    current_question, current_answer, uuid.uuid4(), None)
                print("Question: ")
                print(current_question)
                print("Answer: ")
                print(current_answer)
                current_question = None
                current_answer = None

            else:
                print("ERROR while parsing site!")
                exit(1)
            continue

        # each question is started with a "Nummer X:" paragraph
        if "Nummer " in paragraph.get_text() and paragraph.get_text().endswith(":"):
            i += 1
            print()
            print()
            print("-------------------")
            print(paragraph.get_text())
            notation_counter = 0

            if "Nummer 23:" in paragraph.get_text():
                exit(1)
            continue

        # 'Stand: XXXXXXX' determines the latest update for that page!
        if "Stand: " in paragraph.get_text():
            i += 1
            notation_counter = 0
            continue

        # Either we read a question or an answer...
        if notation_counter == 0:
            # interpret the paragraph as question
            notation_counter += 1
            current_question = paragraph.get_text()

            if paragraph.find_all("img").__len__() != 0:
                print("found image!")
                print(paragraph.find_all("img").__len__())
                for img in paragraph.find_all("img"):
                    print(img.attrs["src"])
                    download_image(
                        img.attrs["src"], 'images/', img.attrs["src"].split("/")[-1].split("?")[0])

                    # TODO download images here!
                # TODO if multiple images, combine them into one image
                # TODO calculate base 64 value for image
                # TODO set image base 64 value for card.
                exit(1)
        elif notation_counter == 1:
            # interpret the paragraph as answer
            notation_counter += 1
            current_answer = paragraph.get_text()
        elif notation_counter > 1:
            # interpret the paragraph as answer
            notation_counter += 1
            current_answer += " " + paragraph.get_text()

        i += 1
