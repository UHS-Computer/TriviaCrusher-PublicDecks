
import os
import urllib3


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
