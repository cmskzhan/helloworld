import csv

CompanyName="MICROSOFT CORP"
data = {}
filename="/home/sroot/kaizha/github/helloworld/concepts/sec-cik-lookup-chopped.txt"

with open(filename, mode='r') as infile:
    reader = csv.reader(infile, delimiter=':')
    data = {row[0]:row[1] for row in reader} # if csv has header, use row['key']:row['value']
    # for row in reader:
    #     data.update({row[0]:row[1]})
        

if CompanyName in data.keys():
    print(data[CompanyName])

