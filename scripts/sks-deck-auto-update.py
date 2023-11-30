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

path_to_tcjson_file = "./de_DE/categories/freizeit/sks/sks-deck.tcjson"
path_to_md_file = "./de_DE/categories/freizeit/sks/sks-deck.md"
path_for_images = "./de_DE/categories/freizeit/sks/images"

# the deck SKS consists of of 5 parts which are combined into one big deck here!
urls_to_scan = [
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Navigation/Navigation-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Schifffahrtsrecht/Schifffahrtsrecht-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Wetterkunde/Wetterkunde-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Seemannschaft-I/Seemannschaft-I-node.html",
    "https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Seemannschaft-II/Seemannschaft-II-node.html",
]


def gif2jpg(file_path: str, file_name: str, num_key_frames: int, trans_color: tuple) -> List[str]:
    """
    convert gif to `num_key_frames` images with jpg format
    :param file_name: gif file name
    :param num_key_frames: result images number
    :param trans_color: set converted transparent color in jpg image
    :return:
    """
    result = []
    with Image.open(file_path + file_name) as im:
        for i in range(num_key_frames):
            im.seek(im.n_frames // num_key_frames * i)
            image = im.convert("RGBA")
            datas = image.getdata()
            newData = []
            for item in datas:
                if item[3] == 0:  # if transparent
                    newData.append(trans_color)  # set transparent color in jpg
                else:
                    newData.append(tuple(item[:3]))
            image = Image.new("RGB", im.size)
            image.getdata()
            image.putdata(newData)
            new_file_name = file_name.split(".")[0].replace("gif",
                                                            "jpg") + '_{}.jpg'.format(i)
            image.save(file_path + '/'+new_file_name)
            result.append(file_path + '/'+new_file_name)
    return result


def download_image(url, file_path, file_name):
    # Check whether the specified path exists or not
    isExist = os.path.exists(file_path)
    # printing if the path exists or not
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(file_path)

    full_path = file_path + file_name
    # urllib3.request.urlretrieve(url, full_path)

    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)

    with open(full_path, 'wb') as out:
        while True:
            data = r.read()
            if not data:
                break
            out.write(data)

    r.release_conn()


result = Deck(
    id=uuid.UUID('8f2274f7-889b-4874-aac7-92a6dc0ef16d'),
    name="SKS - Sportküstenschifferschein Theorie Fragen",
    description="Dies sind die Lernzettel für den SKS - Sportküstenschifferschein.\nHierzu wurden die offiziellen Prüfungsfragen von <https://www.elwis.de/> in Karteikarten übersetzt.\n\n\nStand des Exports ist: ",
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
    current_answer: str | None = None
    current_base64_image_str: str | None = None
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
                    current_question, current_answer, current_base64_image_str)
                current_question = None
                current_answer = None
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
            current_answer = paragraph.get_text()
        elif notation_counter > 1:
            # interpret the paragraph as answer
            notation_counter += 1
            current_answer += " " + paragraph.get_text()

        i += 1

f = open(path_to_tcjson_file, 'w')
f.write(json.dumps(result, indent=2))
f.close()

f = open(path_to_md_file, 'w')
f.write(result.__markdown__(path_for_images))
f.close()
