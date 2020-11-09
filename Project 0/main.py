from location import Location
from road import Road


def main():

    # Retrieve filename from user
    filename = str(input("Please enter a filename: "))

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

    # while loop switch
    quit = 1

    # grab user locations
    while quit != 0:
        userLocation = input("Please enter a location or 0 to quit: ")

        if userLocation != "0":
            locationID = str(userLocation)

            print("Location {} has edges leading to: ".format(locationID))

            # loop roadList and print minding start / end IDs
            roadList = roadDict[locationID]
            for road in roadList:
                if locationID == road.startID:
                    print("{}\t{} mph\t{}".format(road.endID, road.speedLimit, road.name))
                else:
                    print("{}\t{} mph\t{}".format(road.startID, road.speedLimit, road.name))

        else:
            quit = 0

    return 0


if __name__ == "__main__":
    main()
