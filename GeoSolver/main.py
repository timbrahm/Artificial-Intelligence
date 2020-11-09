import os
import urllib.request
import urllib.parse
import matplotlib as mp
import numpy as np
import itertools
import requests
import js2py

from matplotlib.pyplot import imread
from location import Location

TEST = mp.pyplot.imread("./TestImage.jpg")


def GetStreet(location, key, save):
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
    MyUrl = base + urllib.parse.quote_plus(location) + key
    filename = location + ".jpg"
    rv = urllib.request.urlretrieve(MyUrl, os.path.join(save, filename))
    return rv

def parseImgs(path):
    mainDir = os.path.dirname(__file__)
    relPath = path
    absPath = os.path.join(mainDir, relPath)

    loclist = []
    if os.path.isdir(absPath):
        directory = os.fsencode(absPath)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            lat = filename.split(",")[0]
            long = filename.split(",")[1][:-4]

            img = mp.pyplot.imread(os.path.join(absPath, filename))
            if not np.array_equal(TEST, img):
                newLoc = Location(img, lat, long)
                loclist += [newLoc]
    elif os.path.isfile(absPath):
        img = mp.pyplot.imread(absPath)
        if not np.array_equal(TEST, img):
            loclist += img
    else:
        img = None

    return loclist

def main():
    path = r"./locations"
    key = "&key={}".format(os.environ['KEY'])

    location = "46.376180,9.228132"
    # check = GetStreet(location, key, path)

    locList = parseImgs(path)

    # print(locList)
    #
    # url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}{}".format(locList[1].lat, locList[1].long, key)
    # rv = requests.get(url)
    #
    # print(rv)
    # print(os.fsdecode(rv.content))

    js = """
    var output = 5
    output += 10
    return output
    """


    context = js2py.EvalJs()
    context.execute(js)
    print(context.output)


    return 0


if __name__ == "__main__":
    main()
