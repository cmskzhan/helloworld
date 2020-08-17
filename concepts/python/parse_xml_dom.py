import xml.dom.minidom
import requests
# import xml.etree.ElementTree as ET


proxy = {

    "http": "http://se10cbcsg01.org.nasdaqomx.com:8080",
    "https": "http://se10cbcsg01.org.nasdaqomx.com:8080"
}


cik = ['0000789019']
for i in cik:
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + i + '&type=10-Q&count=1&output=atom'
    xml1result=requests.get(url, verify=False)
    dom3 = xml.dom.minidom.parseString(xml1result.text)
    print(dom3.documentElement.tagName)

    it2 = dom3.getElementsByTagName('accession-number')
    for i in it2: 
    #print(i.toxml())
        print(i.firstChild.data)