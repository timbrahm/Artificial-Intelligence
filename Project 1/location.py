class Location:

    def __init__(self, ID, long, lat):
        self.ID = ID
        self.lat = lat
        self.long = long
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = 0


    def update_g(self, newg):
        self.g = newg

    def update_h(self, newh):
        self.h = newh

    def update_f(self, newf):
        self.f = newf

    def set_parent(self, newParent):
        self.parent = newParent
