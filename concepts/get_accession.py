import requests
# import xml.etree.ElementTree as ET
from io import StringIO, BytesIO
from lxml import etree

#cik = ['0000789019', '0001341439']
cik = ['0000789019']
for i in cik:
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + i + '&type=10-Q&count=1&output=atom'
    xmlresult=requests.get(url, verify=False)
    # nons = etree.XMLParser(ns_clean=True)
    # root=etree.fromstring(xmlresult.content, parser=nons)
    root=etree.fromstring(xmlresult.content)
  
    namespace = '{http://www.w3.org/2005/Atom}'
   
    print("root tag:", root.tag, "root attrib:", root.attrib)
    # print([ c.tag for c in root ])

    for item in root.findall(namespace + "entry"): # OR for item in root.xpath("//*[local-name() = 'entry']"):
        print(item[1][0].text)
        #print(item.xpath('//x:content/*', namespaces={'x': '{http://www.w3.org/2005/Atom}'}))

        print(root.xpath("//*[local-name() = 'content']"))
    
   
