import csv
from fuzzywuzzy import process, fuzz

filename="/home/sroot/kaizha/github/helloworld/concepts/sec-cik-lookup-chopped.txt"

data = {}
with open(filename, mode='r') as infile:
    reader = csv.reader(infile, delimiter=':')
    data = {row[0]:row[1] for row in reader} # if csv has header, use row['key']:row['value']
    # for row in reader:
    #     data.update({row[0]:row[1]})
        

companyName=["Gang", "microsoft corp"]
for i in companyName:
    CompanyName = i.upper()
    potential_result=[]
    for company, cik in data.items(): 
        potential_result.append([company, cik, fuzz.partial_ratio(CompanyName, company)])
        potential_result1= sorted(potential_result, key=lambda x: -x[2])

print(potential_result1[0:3])





#######################################
# analyze abnormal lines
#######################################

filename="/home/sroot/kaizha/github/helloworld/concepts/sec-cik-lookup-data.txt"
with open (filename, "r", encoding="latin1") as myfile:
    lines=myfile.read().split("\n")

l=len(lines)-1
for i in reversed(lines):
    semicol = i.count(":")
    if semicol != 2:
        print(lines[l],"has",semicol,"delimiters! Deleting...")
        del lines[l]
    l=l-1

line = [i[:-1] for i in lines]
sec_cik_dictionary = dict(item.split(":") for item in line)
companyName=["MICROSOFT CORP", "ORACLE CORP", "bbb"]


cik=[]
for i in companyName:
    CompanyName = i.upper()
    if CompanyName in sec_cik_dictionary.keys():
        cik.append(sec_cik_dictionary[CompanyName])
    else:
        print(i, "not found in SEC company name. Closest matches below:")
        potential_result=[]
        for company, cik in sec_cik_dictionary.items(): 
            potential_result.append([company, cik, fuzz.partial_ratio(CompanyName, company)])
            # potential_result1= sorted(potential_result, key=lambda x: -x[2])
        print(potential_result[0:2])
    
print(cik)
