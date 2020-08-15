import requests
from lxml import etree
def main():
    #linkedin example
    url="http://httpbin.org/xml"
    result=requests.get(url)
    print(result.text)
    doc = etree.fromstring(result.content)

    print(doc.tag)
    print(doc.attrib['title'])

    for elem in doc.findall("slide"):
        print(elem.tag)
        #print(elem.attrib['item'])

    newSlide=etree.SubElement(doc, "slide")
    newSlide.text="ths is new slide"

    slideCount=len(doc.findall("slide"))
    itemCount=len(doc.findall(".//item")) # find item anywhere in the doc

    print(slideCount, "slide elements in there now")
    print(itemCount, "item element in total")
    print(doc.findall(".//item"))

if __name__=="__main__":
    main()