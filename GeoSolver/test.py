# # import requests
# #
# # key = "AIzaSyCp7rrY9WGUeQPuSBiB9ItmhYcMaODL7Ac"
# #
# # response = requests.get("https://maps.googleapis.com/maps/api/streetview?size=600x300&location=46.414382,10.013988&heading=151.78&pitch=-0.76&key={}".format(key))
# #
# # print(response)
#
# import os
# import urllib.request
# import urllib.parse
#
# myloc = r"./downloads"
# key = "&key=" + "AIzaSyCp7rrY9WGUeQPuSBiB9ItmhYcMaODL7Ac"
#
#
# def GetStreet(Add, SaveLoc):
#     base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
#     MyUrl = base + urllib.parse.quote_plus(Add) + key  # added url encoding
#     fi = Add + ".jpg"
#     urllib.request.urlretrieve(MyUrl, os.path.join(SaveLoc, fi))
#
#
# Tests = ["457 West Robinwood Street, Detroit, Michigan 48203",
#          "1520 West Philadelphia, Detroit, Michigan 48206",
#          "2292 Grand, Detroit, Michigan 48238",
#          "15414 Wabash Street, Detroit, Michigan 48238",
#          "15867 Log Cabin, Detroit, Michigan 48238",
#          "3317 Cody Street, Detroit, Michigan 48212",
#          "14214 Arlington Street, Detroit, Michigan 48212"]
#
# for i in Tests:
#     GetStreet(Add=i, SaveLoc=myloc)


import pycountry_convert as pc

print(pc.country_alpha2_to_continent_code(""))