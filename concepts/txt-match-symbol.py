import difflib
import requests

all_companies_content = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt").content.decode("latin1")
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
cName = "microsoft corp"
print(difflib.get_close_matches("msoft".upper(), all_companies_cik_dict.keys(), n=3, cutoff=0))