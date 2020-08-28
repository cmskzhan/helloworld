# Caveat: this script pulls outstanding shares from SEC 10-Q report. Any Corp event after latest filing date is not accounted
# 0. find company name

# 1. get cik number
# https://www.sec.gov/Archives/edgar/cik-lookup-data.txt

# 2. get accession-number number
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-Q&count=1&output=atom

# 3. parse value from 
# https://www.sec.gov/cgi-bin/viewer?action=view&cik=789019&accession_number=0001564590-20-019706&xbrl_type=v


import requests
# from fuzzywuzzy import process, fuzz
import re
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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

companyName=['microsoft corp', 'oracle corp', 'NASDAQ OMX GROUP, INC.']

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
def accession_no(cikno):
    url10k = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + cikno + '&type=10-K&count=1&output=atom'
    url10q = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + cikno + '&type=10-Q&count=1&output=atom'
    xml10k=requests.get(url10k, verify=False)
    xml10q=requests.get(url10q, verify=False)
    an10k = []
    an10q = []
    for line in xml10k.text.splitlines():
        if re.search('<summary', line):
            for word in line.split():
                an10k.append(word)
    for line in xml10q.text.splitlines():
        if re.search('<summary', line):
            for word in line.split():
                an10q.append(word)
    if an10k[3] > an10q[3]:
        # print(an10k[5],"has date:", an10k[3], "later than", an10q[5],"has date:", an10q[3])
        return an10k[5]
    else: 
        # print(an10q[5],"has date:", an10q[3], "later than", an10k[5],"has date:", an10k[3])
        return an10q[5]
    
acno=[]
for i in cik:
    acno.append(accession_no(i).replace('-',''))
print(acno)


# 3. parse value from 
# https://www.sec.gov/cgi-bin/viewer?action=view&cik=789019&accession_number=0001564590-20-019706&xbrl_type=v
# actually should be 
# https://www.sec.gov/Archives/edgar/data/789019/000156459020019706/R1.htm

for i in range(len(cik)):
    url = 'https://www.sec.gov/Archives/edgar/data/' + cik[i] + '/' + acno[i] + '/R1.htm'
    html = requests.get(url, verify=False)
    soup = BeautifulSoup(html.content, 'lxml')
    td = str(soup.find('td', {'class':"nump"}))
    outstanding_shares = int(''.join(filter(str.isdigit, td))) # extract digits out of string
    print(outstanding_shares)