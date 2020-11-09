from decimal import *
import pprint as pp

getcontext().prec = 8

class LastLocation:
    def __init__(self, m, n, timestep=0):
        self.time_step = timestep
        self.m = Decimal(m)
        self.n = Decimal(n)

        self.location_list = self.genAllRC()
        self.CPT = self.createCPT()

    def __str__(self):
        pp.pprint(self.CPT)
        return ""

    def genAllRC(self):
        location_list = []
        for i in range(int(self.m)):
            for j in range(int(self.n)):
                location_list += [(i, j)]
        return location_list

    def createCPT(self):
        CPT_dict = {}
        for loc in self.location_list:
            CPT_dict[loc] = 1 / (self.m * self.n)

        return CPT_dict

    def updateCPT(self, newCPT):
        self.CPT = newCPT

    def updateTime(self, newTime):
        self.time_step = newTime
