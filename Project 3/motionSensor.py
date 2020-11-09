from decimal import *
import pprint as pp


class MotionSensor:
    def __init__(self, m, n):
        self.m = m
        self.n = n

        self.location_list = self.genAllRC()
        self.m1CPT = self.createCPT("m1")
        self.m2CPT = self.createCPT("m2")

    def __str__(self):
        print("M1 CPT:")
        pp.pprint(self.m1CPT)
        print("M2 CPT:")
        pp.pprint(self.m2CPT)
        return ""

    def genAllRC(self):
        location_list = []
        for i in range(self.m):
            for j in range(self.n):
                location_list += [(i, j)]
        return location_list

    def createCPT(self, mtype):
        CPT = {}
        if mtype == "m1":
            for loc in self.location_list:
                if loc[0] == 0 or loc[1] == 0:
                    prob = Decimal('0.9') - (Decimal('0.1') * (loc[0] + loc[1]))
                    if prob > Decimal('0.05'):
                        CPT[loc] = {True: prob, False: 1 - prob}
                    else:
                        CPT[loc] = {True: Decimal('0.05'), False: Decimal('0.95')}
                else:
                    CPT[loc] = {True: Decimal('0.05'), False: Decimal('0.95')}
        else:
            for loc in self.location_list:
                if loc[0] == self.m - 1 or loc[1] == self.n - 1:
                    prob = Decimal('0.9') - (Decimal('0.1') * ((self.m - 1 + self.n - 1) - (loc[0] + loc[1])))
                    if prob > Decimal('0.05'):
                        CPT[loc] = {True: prob, False: 1 - prob}
                    else:
                        CPT[loc] = {True: Decimal('0.05'), False: Decimal('0.95')}
                else:
                    CPT[loc] = {True: Decimal('0.05'), False: Decimal('0.95')}

        return CPT
