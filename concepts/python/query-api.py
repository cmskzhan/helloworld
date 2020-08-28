import requests

def main():
    #get_xml()
    #post_data_values()
    get_header_values()



def get_xml():
    url="http://httpbin.org/xml"
    result =  requests.get(url) #use requests.get(url, auth=("user","passs")) for basic auth
    print("return code =", result.status_code)
    print("header=",result.headers)
    print(result.content) #result.text for ascii output

def get_data_values():
    url="http://httpbin.org/get"
    keyPairs = {
        "key1": "value1",
        "key2": "value2"
    }
    result = requests.get(url, params=keyPairs)
    print(result.content)

def get_header_values():
    url="http://httpbin.org/get"
    header = {
        "User-Agent": "Kai test App 0.0.1"
    }
    result = requests.get(url, headers=header)
    print(result.headers)
    print(result.content)

def post_data_values():
    url="http://httpbin.org/post"
    keyPairs = {
        "key1": "value1",
        "key2": "value2"
    }
    result = requests.post(url, data=keyPairs)
    print(result.content)


if __name__=="__main__":
    main()