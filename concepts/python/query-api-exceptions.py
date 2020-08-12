import requests
from requests import HTTPError, Timeout

def main():
    try_timeout()


def try_404():
    url="http://httpbin.org/status/404"
    try:
        result=requests.get(url)
        result.raise_for_status() # o/w it won't report err
        print(result.status_code, result.headers, result.content)
    except HTTPError as err:
        print("Err: {0}", format(err))


def try_timeout():
    url="http://httpbin.org/delay/9"
    try:
        result=requests.get(url, timeout=5)
        result.raise_for_status() # o/w it won't report err
        print(result.status_code, result.headers, result.content)
    except HTTPError as err:
        print("Err: {0}", format(err))
    except TimeoutError as err:
        print("Request Timeout: {0}", format(err))



if __name__=="__main__":
    main()