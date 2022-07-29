import os
import re
import requests
import sys
import tqdm

"""Sraping naughty pix to local hard drive, 
    requires forum thread page to scrape
    destionation directory to save images is hard coded"""


def download_image(url, dl_folder):
    filename = url.split('/')[-1]
    response = requests.get(url, stream=True)
    with open(os.path.join(dl_folder, filename), 'wb') as out_file:
        out_file.write(response.content)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scrape_npix.py <forum thread page>")
        sys.exit(1)

    for i in sys.argv:
        # if i is a valid url
        if re.match(r'^(http|https)://', i):
            forum_thread_url = i
            foldername= forum_thread_url.split('/')[-1].split('.')[0]

            if os.name == 'nt':
                destination = r"F:\Downloads\samples\met-art\scraped\{}".format(foldername)
            else:
                destination = r"/mnt/4thdd/download/18plus/{}".format(foldername)
            if not os.path.exists(destination):
                os.makedirs(destination)
            print(f"Scraping {forum_thread_url} to {destination}")
            r = requests.get(forum_thread_url)
            jpg_urls = re.findall(r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+.jpg', r.text)
            for url in tqdm.tqdm(jpg_urls):
                download_image(url, destination)
        else:
            print(f"{i} is not a valid url, skipping this parameter!")
            continue
        





