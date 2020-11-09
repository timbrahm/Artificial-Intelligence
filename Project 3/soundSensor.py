from decimal import *
import pprint as pp


class SoundSensor:
    def __init__(self, m, n):
        self.m = m
        self.n = n

        self.location_list = self.genAllRC()
        self.CPT = self.createCPT()
        self.sortCPT()

    def __str__(self):
        pp.pprint(self.CPT)
        return ""

    def createCPT(self):
        CPT = {}
        for loc in self.location_list:
            man1_moves = self.gen1ManRC(loc[0], loc[1])
            man2_moves = self.gen2ManRC(loc[0], loc[1])
            for i in range(self.m):
                for j in range(self.n):
                    move = (i, j)
                    if move == loc:
                        if loc not in CPT:
                            CPT[loc] = {move: Decimal('0.6')}
                        else:
                            CPT[loc][move] = Decimal('0.6')
                    elif move in man1_moves:
                        if loc not in CPT:
                            CPT[loc] = {move: (Decimal('0.3') / len(man1_moves))}
                        else:
                            CPT[loc][move] = (Decimal('0.3') / len(man1_moves))
                    elif move in man2_moves:
                        if loc not in CPT:
                            CPT[loc] = {move: (Decimal('0.1') / len(man2_moves))}
                        else:
                            CPT[loc][move] = (Decimal('0.1') / len(man2_moves))
                    else:
                        if loc not in CPT:
                            CPT[loc] = {move: Decimal(0)}
                        else:
                            CPT[loc][move] = Decimal(0)
        return CPT

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

    def gen2ManRC(self, r, c):
        location_list = []
        r1 = [r - 1, r + 1, r - 2, r + 2]
        c1 = [c - 1, c + 1, c - 2, c + 2]

        for i in range(2):
            for j in range(2):
                if 0 <= r1[i] <= self.m - 1 and 0 <= c1[j] <= self.n - 1:
                    if (r1[i], c1[j]) not in location_list:
                        location_list += [(r1[i], c1[j])]
        for i in range(2, 4):
            for j in range(2, 4):
                if 0 <= r1[i] <= self.m - 1:
                    if (r1[i], c) not in location_list:
                        location_list += [(r1[i], c)]
                if 0 <= c1[j] <= self.n - 1:
                    if (r, c1[j]) not in location_list:
                        location_list += [(r, c1[j])]

        return location_list

    def sortCPT(self):
        for curr_loc in self.CPT:
            temp = self.CPT[curr_loc]
            temp = {k: v for k, v in reversed(sorted(temp.items(), key=lambda item: item[1]))}
            self.CPT[curr_loc] = temp
