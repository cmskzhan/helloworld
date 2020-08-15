# Caveat: this script pulls outstanding shares from SEC 10-Q report. Any Corp event after latest filing date is not accounted
# 0. find company name

# 1. get cik number
# https://www.sec.gov/Archives/edgar/cik-lookup-data.txt

# 2. get accession-number number
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-Q&count=1&output=atom

# 3. parse value from 
# https://www.sec.gov/cgi-bin/viewer?action=view&cik=789019&accession_number=0001564590-20-019706&xbrl_type=v


import requests
from fuzzywuzzy import process, fuzz

all_companies_page = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt", verify=False)
all_companies_content = all_companies_page.content.decode("latin1")
all_companies_array = all_companies_content.split("\n")

# remove records that can't be converted to dictionary (has : in companyname)
l=len(all_companies_array)-1
for i in reversed(all_companies_array):
    semicol = i.count(":")
    if semicol != 2:
        # print(all_companies_array[l],"has",semicol,"delimiters! Deleting...")
        del all_companies_array[l]
    l=l-1

all_companies_arra = [i[:-1] for i in all_companies_array] #remove trailing :
all_companies_cik_dict=dict(item.split(":") for item in all_companies_arra)

companyName=["microsoft corp", "oracle corp", "bbb"]

# 1. get cik number
cik=[]
for i in companyName:
    CompanyName = i.upper()
    if CompanyName in all_companies_cik_dict.keys():
        cik.append(all_companies_cik_dict[CompanyName])
    else:
        print(i, "not found in SEC company name. ") # Closest matches below:")
        # potential_result=[]
        # for company, cik in all_companies_cik_dict.items(): 
        #     potential_result.append([company, cik, fuzz.partial_ratio(CompanyName, company)])
        #     potential_result1= sorted(potential_result, key=lambda x: -x[2])
        # print(potential_result1[0])
        # print(potential_result1[1])
    
print(cik)

# 2. get accession-number number
for i in cik:
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + i + '&type=10-Q&count=1&output=atom'
    xmlresult=requests.get(url, verify=False)
    for line in xmlresult.text.splitlines():
        if re.search('<summary', line):
            print(line)

