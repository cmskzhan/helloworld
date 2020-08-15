import xml.etree.ElementTree as ET
import requests

cik = ['0000789019', '0001341439']
for i in cik:
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + i + '&type=10-Q&count=1&output=atom'
    xmlresult=requests.get(url, verify=False)
    root=ET.fromstring(xmlresult.content)
    print(root.tag, root.attrib)
    for child in root:
        for grandchild in child:
            print(grandchild.tag, grandchild.text)