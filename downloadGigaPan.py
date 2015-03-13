#usage: python downloadGigaPan.py <photoid>
# http://gigapan.org/gigapans/<photoid>>

from xml.dom.minidom import *
from urllib2 import *
from urllib import *
import sys,os,math

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def find_element_value(e,name):
    nodelist = [e]
    while len(nodelist) > 0 :
        node = nodelist.pop()
        if node.nodeType == node.ELEMENT_NODE and node.localName == name:
            return getText(node.childNodes)
        else:
            nodelist += node.childNodes

    return None


#main

photo_id = int(sys.argv[1])
if not os.path.exists(str(photo_id)):
    os.makedirs(str(photo_id))

base = "http://www.gigapan.org"

# read the kml file
h = urlopen(base+"/gigapans/%d.kml"%(photo_id))
photo_kml=h.read()


# find the width and height, level 
dom = parseString(photo_kml)

height=int(find_element_value(dom.documentElement, "maxHeight"))
width=int(find_element_value(dom.documentElement, "maxWidth"))
tile_size=int(find_element_value(dom.documentElement, "tileSize"))

print width,height,tile_size


maxlevel = max(math.ceil(width/tile_size), math.ceil(height/tile_size))
maxlevel = int(math.ceil(math.log(maxlevel)/math.log(2.0)))
wt = int(math.ceil(width/tile_size))+1
ht = int(math.ceil(height/tile_size))+1
print wt,ht,maxlevel

#loop around to get every tile
for j in xrange(ht):
    for i in xrange(wt):
        filename = "%04d-%04d.jpg"%(i,j)
        url = "%s/get_ge_tile/%d/%d/%d/%d"%(base,photo_id, maxlevel,j,i)
        print url, filename
        h = urlopen(url)
        fout = open(str(photo_id)+"/"+filename,"wb")
        fout.write(h.read())
        fout.close()
