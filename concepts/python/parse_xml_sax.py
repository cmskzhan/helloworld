# get accession-number number by parsing XML data using the SAX parser
# caveat, doesn't return only print
import requests
import xml.sax
from datetime import datetime
import operator

class the10QHandler(xml.sax.ContentHandler): # Users are expected to subclass ContentHandler to support their application
    def __init__(self):
        self.currentTag = ""
        self.fileCount = 0
        self.accessionNumber = ""
        self.filingDate = ""
        self.accessionNumberResults =[]
        self.filingDateResults=[]

# list of methods to overload is https://docs.python.org/2/library/xml.sax.handler.html 19.12.1. ContentHandler Objects
# key ones are listed below
    def startElement(self, tagName, attrs):
        if tagName == "content":
            # print("content type " + attrs['type'])
            self.fileCount += 1
        self.currentTag = tagName

    def characters(self, content):
        if self.currentTag ==  'accession-number':
            self.accessionNumber = content
        elif self.currentTag == 'filing-date':
            self.filingDate = content


    def endElement(self, tagName):
        if tagName == "content":
            print(self.fileCount, "10-Q documents found")
        elif tagName == 'accession-number':
            print("accession number:", self.accessionNumber)
            self.accessionNumberResults.append(self.accessionNumber)
        elif tagName == 'filing-date':
            print("filing date:", self.filingDate)
            self.filingDateResults.append(self.filingDate)


    def startDocument(self):
        print("Start Parsing RSS xml from SEC EDGAR")


    def endDocument(self):
        filingDates = []
        for date in self.filingDateResults:
            filingDates.append(datetime.strptime(date, '%Y-%m-%d'))
        print(filingDates, self.accessionNumberResults)
        index, value = max(enumerate(filingDates), key=operator.itemgetter(1))
        print(self.accessionNumberResults[index], 'is the latest report filed on', value)
        return self.accessionNumberResults[index]

        


def main():

    # create a new content handler for the SAX parser
    handler = the10QHandler()

    # use the Requests lib to get XML data from the server
    # remember that Requests auto-decodes our content
    cik = ['0000789019']
    for i in cik:
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + i + '&type=10-Q&count=1&output=atom'
        xmlresult=requests.get(url, verify=False)
        xml.sax.parseString(xmlresult.text, handler)


if __name__ == "__main__":
    main()
