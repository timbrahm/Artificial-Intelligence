from location import Location
from road import Road

def parse_map(filename):
    # initialize location dictionary {ID -> Location} and road dictionary {ID -> list[Road]}
    locationDict = {}
    roadDict = {}

    # parse file
    with open(filename, "r") as file:
        for line in file:
            # remove \n and split line by delimiter
            line = line.rstrip()
            splitLine = line.split("|")

            # create new Location instances for "location" lines and add them to locationDict
            if splitLine[0] == "location":
                newLocation = Location(splitLine[1], splitLine[2], splitLine[3])
                locationDict[splitLine[1]] = newLocation

            # create new Road instances for "road" lines and add them to roadDict
            elif splitLine[0] == "road":
                newRoad = Road(splitLine[4], splitLine[3], splitLine[1], splitLine[2])

                if splitLine[1] in roadDict.keys():
                    roadDict[splitLine[1]] += [newRoad]
                else:
                    roadDict[splitLine[1]] = [newRoad]

                if splitLine[2] in roadDict.keys():
                    roadDict[splitLine[2]] += [newRoad]
                else:
                    roadDict[splitLine[2]] = [newRoad]

        file.close()
    return locationDict, roadDict
