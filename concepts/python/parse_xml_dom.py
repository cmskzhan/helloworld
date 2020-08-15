import xml.dom.minidom
import requests
# import xml.etree.ElementTree as ET



def main():
    url="http://httpbin.org/xml"
    result=requests.get(url)


    # Parse result into dom tree    
    domtree = xml.dom.minidom.parseString(result.text)
    rootnode = domtree.documentElement

    # display info about the content
    print("Root element is ", rootnode.nodeName)
    print("Title: ", rootnode.getAttribute('title'))

    items = domtree.getElementsByTagName("item")
    print(items.length, " item tags in xml")


# <slideshow 
#     title="Sample Slide Show"
#     date="Date of publication"
#     author="Yours Truly"
#     >

#     <!-- TITLE SLIDE -->
#     <slide type="all">
#       <title>Wake up to WonderWidgets!</title>
#     </slide>

#     <!-- OVERVIEW -->
#     <slide type="all">
#         <title>Overview</title>
#         <item>Why <em>WonderWidgets</em> are great</item>
#         <item/>
#         <item>Who <em>buys</em> WonderWidgets</item>
#     </slide>

# </slideshow>

# add new tag
    newItem=domtree.createElement("item")
    newItem.appendChild(domtree.createTextNode("Add test text under item"))
# add something under first slide
    firstSlide=domtree.getElementsByTagName("slide")[0]
    firstSlide.appendChild(newItem)

    #newItem.appendChild(domtree.createTextNode("Add more text under item of 2nd slide"))
    secondSlide=domtree.getElementsByTagName("slide")[1]
    secondSlide.appendChild(newItem)

    items = domtree.getElementsByTagName("item")
    print(items.length, " item tags in xml")

    xmlcontent=domtree.toxml()
    print(xmlcontent)

    # parse xmlcontent 
    domtree_new = xml.dom.minidom.parseString(xmlcontent)
    rootnode_new = domtree_new.documentElement

    print(getNodeText(domtree_new))
    # for slides in rootnode_new.getElementsByTagName("slide"):
    #     title = slides.getElementsByTagName('title')
    #     print(title[0].firstChild.data)
    #     print("values:", getNodeText(slides))

    

def getNodeText(node):

    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

if __name__=="__main__":
    main()