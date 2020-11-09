class Location:
    def __init__(self, img, lat, long):
        self.img = img
        self.lat = lat
        self.long = long

    def __str__(self):
        return "({}, {})".format(str(self.lat), str(self.long))

    def __repr__(self):
        return "({}, {})".format(str(self.lat), str(self.long))