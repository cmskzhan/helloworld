import requests
import threading
import logging
import time

FORMAT = "[%(asctime)s, %(threadName)s, %(levelname)s] %(funcName)s ,%(message)s"
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format=FORMAT, filemode='a')

class PokeURLs():
    def __init__(self):
        self.dl_lock = threading.Lock()
        max_concurrent_dl = 4
        self.dl_sem = threading.Semaphore(max_concurrent_dl)
        self.result = {}

    def PokeyMon(self, url):
        self.dl_sem.acquire()
        try:
            logging.info("Poking at URL: " + url)
            response = requests.get(url)
            self.result[url] = response.status_code
        except Exception as e:
            self.result[url] = type(e)
        finally:
            self.dl_sem.release()
        

    def PokeURLs(self, url_list):
        if not url_list:
            return
        logging.info("beginning poking URLs")
        start = time.perf_counter()
        threads = []
        for url in url_list:
            t = threading.Thread(target=self.PokeyMon, args=(url,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        end = time.perf_counter()

        logging.info(f"Poked {len(url_list)} links in {end - start} seconds")
        print(self.result)


URLS = \
    ['https://dl.dropboxusercontent.com',
     'https://www.bbc.co.uk',
     'https://www.cnn.com',
     'https://www.yahoo.com',
     'https://www.github.com',
     'https://example.com',
     'https://www.mwam.com',
     'https://www.vanguardinvestor.co.uk',
     'https://www.wenxuecity.com',
     'https://fishandchips.fans/',
     'https://www.hotukdeals.com/',
     'http://rijo34w.com/'
    ]

tt = PokeURLs()
tt.PokeURLs(URLS)