import httpx
import asyncio
from datetime import datetime
import re
import os
import sys

async def get_npix(url, dlfolder):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        jpg_urls = re.findall(r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+.jpg', r.text)
        resps = await asyncio.gather(*map(download_image, jpg_urls, [dlfolder]*len(jpg_urls)))
        for resp in resps:
            if resp.status_code == 200:
                print(f"{resp.url} downloaded successfully!")
            else:
                print(f"{resp.url} failed with {resp.status_code}!")
        # for url in jpg_urls:
        #     resps = await asyncio.gather(download_image(url, dlfolder))
        #     await download_image(url, dlfolder)

async def download_image(url, dlfolder):
    filename = url.split('/')[-1]
    print(filename)
    async with httpx.AsyncClient() as client:
        r = await client.get(url, follow_redirects=True)
        with open(os.path.join(dlfolder, filename), 'wb') as out_file:
            out_file.write(r.content)
    return r



async def main():
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
            await get_npix(forum_thread_url, destination)
            
        else:
            print(f"{i} is not a valid url, skipping this parameter!")
            continue

if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(main())
    end = datetime.now()
    print(f"Total time: {end - start}")