from collections import Counter
import requests

def main():
    all_companies_page = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt", verify=False)
    all_companies_content = all_companies_page.content.decode("latin1")
    lines = all_companies_content.split("\n")

    # filename="/home/sroot/kaizha/github/helloworld/concepts/sec-cik-lookup-data.txt"
    # with open (filename, "r", encoding="latin1") as myfile:
    #     lines=myfile.read().split("\n")
    

    cleaned = [cleanlist for cleanlist in lines if cleanlist.count(":") == 2] #remove list that can't be converted to dictionary
    lines = [i[:-1] for i in cleaned] # remove trailing semi colon
    # flatten the lines list
    flatten = []
    for block in lines:
        for c in block.split(":"):
            flatten.append(c)

    res = dict(Counter(flatten)) #calculate occurances of each list element

    
    for (key, value) in res.items():
        if not key.isdigit():
            if value > 2:
                print(key, value)

    # dict_companies = dict(item.split(":") for item in lines) # convert list to dictionary   
    # res = dict(Counter(dict_companies.values())) # calculate dupliation in dict values


if __name__=="__main__":
    main()