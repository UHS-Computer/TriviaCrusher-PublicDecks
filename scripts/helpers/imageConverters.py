from PIL import Image
from PIL import GifImagePlugin
from typing import List


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
