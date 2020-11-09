from decimal import *
import pprint as pp


class CurrentLocation:
    def __init__(self, m, n):
        self.m = m
        self.n = n

        self.location_list = self.genAllRC()
        self.CPT = self.createCPT()

    def __str__(self):
        for last in self.CPT:
            for curr in self.CPT[last]:
                print("P(C = {} | L = {}) = {}".format(curr, last, self.CPT[last][curr]))
            print()
        return ""

    def genAllRC(self):
        location_list = []
        for i in range(self.m):
            for j in range(self.n):
                location_list += [(i, j)]
        return location_list

    def gen1ManRC(self, r, c):
        location_list = []
        r1 = [r - 1, r + 1]
        c1 = [c - 1, c + 1]

        for i in range(2):
            if 0 <= r1[i] <= self.m - 1:
                if (r1[i], c) not in location_list:
                    location_list += [(r1[i], c)]
            if 0 <= c1[i] <= self.n - 1:
                if (r, c1[i]) not in location_list:
                    location_list += [(r, c1[i])]

        return location_list

    def createCPT(self):
        CPT = {}
        for loc in self.location_list:
            move_list = self.gen1ManRC(loc[0], loc[1])
            for i in range(self.m):
                for j in range(self.n):
                    move = (i, j)
                    if move not in move_list:
                        if loc in CPT:
                            CPT[loc][move] = 0
                        else:
                            CPT[loc] = {move: 0}
                    else:
                        if loc in CPT:
                            CPT[loc][move] = 1 / Decimal(len(move_list))
                        else:
                            CPT[loc] = {move: 1 / Decimal(len(move_list))}

        return CPT

    def getDistrib(self, last):
        last_distrib = (last, self.CPT[last])

        return last_distrib

    def getProb(self, curr, last):
        last_prob = (curr, last, self.CPT[last][curr])

        return last_prob
