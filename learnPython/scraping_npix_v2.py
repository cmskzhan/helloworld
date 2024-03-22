import re
import requests
import sys
import os

# scrape links from https://hjd2048.com/2048/thread.php?fid=25 to r"F:\Downloads\samples\scraped" or 


def donwload_images_to_folder(folder: str, result: list):
    count = 1
    total = len(result)
    for i in result:
        extract_url = i.split('"')[1]
    # download image
        response = requests.get(extract_url)
    # save image to folder
        with open(os.path.join(folder, extract_url.split("/")[-1]), "wb") as f:
            f.write(response.content)
            print(f"Downloaded {extract_url.split('/')[-1]} to {folder}, {count} of {total}")
            count += 1


if len(sys.argv) < 2:
    print("No url provided")
    sys.exit()
elif "-h" in sys.argv:
    print("Usage: python newsite.py url")
    print("Prints error message when url is not valid")
    sys.exit()
else:
    if os.name == "nt":
        abs_path = r"F:\Downloads\samples\scraped"
    else:
        abs_path = r"/mnt/4thdd/download/18plus"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    for url in sys.argv:
        if re.match(r'^(http|https)://', url):
            # create folder base on the last part of the url
            folder = url.split("?")[-1]
            folder = folder.replace("=", "_")
            folder = os.path.join(abs_path, folder)
            try:
                os.mkdir(folder)
            except FileExistsError:
                print(f"Folder {folder} already exists, probably becasue {url} has been downloaded before, skipping {url}")
                continue

            response = requests.get(url, headers=headers)
            html_str = response.text
            pattern = re.compile(r'src=\"https://.*?\.(?:png|jpg)')
            image_urls = pattern.findall(html_str)
            donwload_images_to_folder(folder, image_urls)

        else:
            print(f"{url} is not a valid url, skipping this parameter!")
            continue