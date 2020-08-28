import json
from json import JSONDecodeError

import requests

def main():
    jsonStr= '''{
        "FirstName": "Ray",
        "Manager": true,
        "Title": "Mr",
        "Address": [ 
            "111 high street",
            "Milton Keynes",
            "MK15 8HD"
        ],
        "Salary": 31231.34
    }'''

    parse_json(jsonStr)

    dict_to_json = {
        "CompanyName": "Apple",
        "US": True,
        "Branches": ["London","China","Singapore"],
        "CommonShares": 4275634
    }
    jsonStr=json.dumps(dict_to_json, indent=5) # pretty print with indent space = 5 from dict to json
    print(jsonStr)

    # let's try some exceptions
    jsonStr= '''{
        "FirstName": "Ray"
        "Manager": true,
        "Title": "Mr",
        "Address": [ 
            "111 high street",
            "Milton Keynes",
            "MK15 8HD"
        ],
        "Salary": 31231.34
    }'''   # miss a comma from first line
    try:
        data = json.loads(jsonStr)
    except JSONDecodeError as jerr:
        print("shit! ", jerr.msg)
        print(jerr.lineno, jerr.colno)

    # let's try json from httpbin
    url = "http://httpbin.org/json"
    result = requests.get(url, verify=False)
    dict_data = result.json() # this is already dict
    print(dict_data)  # this is already dict
    print(list(dict_data.keys()))
    print(dict_data['slideshow']['title'])



def parse_json(abc):
    data=json.loads(abc)
    print("NickName:", data['FirstName'])
    if (data['Manager']):
        print("not a worker")
    for addr in data["Address"]:
        print("Lives on " + addr)

if __name__=="__main__":
    main()



