import pycountry_convert as pc
import pprint as pp


class Location:
    def __init__(self, img, lat, long):
        self.img = img
        self.lat = lat
        self.long = long

        self.address = None
        self.continent = None
        self.country, self.country_code = None, None
        self.locality = None
        self.admin_levels = [None, None, None, None, None]
        self.plus_code = None

        self.JSON = None

    def __str__(self):
        if self.JSON:
            pp.pprint(self.JSON)
            return ""
        else:
            return "({}, {})".format(str(self.lat), str(self.long))

    def __repr__(self):
        return "({}, {})".format(str(self.lat), str(self.long))

    def toJSON(self):
        obj = {}
        obj["image"] = self.img
        obj["coords"] = {
            "lat": self.lat,
            "long": self.long
        }
        obj["geo_details"] = {
            "address": self.address,
            "locality": self.locality,
            "admin_levels": {
                "1": self.admin_levels[0],
                "2": self.admin_levels[1],
                "3": self.admin_levels[2],
                "4": self.admin_levels[3],
                "5": self.admin_levels[4]
            },
            "country": {
                "name": self.country,
                "country_code": self.country_code
            },
            "continent": self.continent,
            "plus_code": self.plus_code
        }

        self.JSON = obj
        return obj

    def setAddress(self, address):
        self.address = address

    def setContinent(self, continent):
        self.continent = continent

    def setCountry(self, country, country_code):
        self.country = country
        self.country_code = country_code

    def setLocality(self, locality):
        self.locality = locality

    def setAdminLevels(self, admin_type, level_name):
        self.admin_levels[admin_type - 1] = level_name

    def setPlusCode(self, plus_code):
        self.plus_code = plus_code

    def setContinent(self):
        self.continent = pc.country_alpha2_to_continent_code(self.country_code)

    def setJSON(self):
        self.toJSON()
