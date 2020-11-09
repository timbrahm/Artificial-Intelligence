from parseMap import parse_map
from sphereDistance import distance_on_unit_sphere
from priorityQueue import PriorityQueue

# Global Debug Constant
DEBUG = False


def a_star(locationDict, roadDict, startID, goalID):
    # count expanded nodes
    expanded_count = 0

    # initialize frontier pqueue and explored list
    frontier = PriorityQueue()
    explored = []

    # add start location to frontier
    frontier.push(startID, 0)

    # select goal location object for h calculations later
    goalLocation = locationDict[goalID]

    # loop through frontier until empty
    while len(frontier.pq) > 0:
        # select location with lowest f in pqueue
        nodeID = frontier.pop()
        node = locationDict[nodeID]

        # debug option
        if DEBUG:
            print("Visiting {}, g={}, h={}, f={}".format(nodeID, node.g * 60, node.g * 60, node.f * 60))

        # iterate count
        expanded_count += 1

        # check if goal state
        if nodeID == goalID:
            break

        # find all roads connected to selected location
        roadList = roadDict[node.ID]
        for road in roadList:
            # have to check both start and end IDs to make sure selection is correct in calculations
            if node.ID == road.startID:
                if road.endID not in explored:

                    # road.endID is the ID of the adjacent node
                    adjNode = locationDict[road.endID]

                    # calculate adjacent distance using sphere calc
                    adjDist = (distance_on_unit_sphere(node.lat, node.long, adjNode.lat, adjNode.long)) * 3960
                    # convert to time and add to previous g
                    g = node.g + (adjDist / float(road.speedLimit))

                    # calculate h based on goal node
                    hDist = (distance_on_unit_sphere(adjNode.lat, adjNode.long, goalLocation.lat, goalLocation.long)) * 3960
                    h = hDist / 65

                    f = g + h

                    # if adjacent node not in priority queue
                    if adjNode.ID not in frontier.entry_finder:
                        frontier.push(adjNode.ID, f)
                        # update adjacent node object's features
                        adjNode.set_parent(node.ID)
                        adjNode.update_g(g)
                        adjNode.update_h(h)
                        adjNode.update_f(f)

                        # debug option
                        if DEBUG:
                            print("\tAdding {}, g={}, h={}, f={} to the frontier.".format(adjNode.ID, adjNode.g * 60,
                                                                                         adjNode.h * 60, adjNode.f * 60))

                    # if adjacent node's f is less than its current f in priority queue
                    elif f < frontier.entry_finder[adjNode.ID][0]:
                        # debug options
                        if DEBUG:
                            print("\t Updating path cost for {} on the frontier.".format(adjNode.ID))
                            print("\t\told: g={}, h={}, f={}".format(adjNode.g * 60, adjNode.h * 60, adjNode.f * 60))

                        frontier.push(adjNode.ID, f)
                        # update adjacent node object's features
                        adjNode.set_parent(node.ID)
                        adjNode.update_g(g)
                        adjNode.update_h(h)
                        adjNode.update_f(f)

                        # debug options
                        if DEBUG:
                            print("\t\tnew: g={}, h={}, f={}".format(adjNode.g * 60, adjNode.h * 60, adjNode.f * 60))

                    else:
                        # if adjacent node's f is more than its current f in priority queue
                        continue

                else:
                    # node is already explored
                    continue

            else:
                if road.startID not in explored:
                    # road.startID is the ID of the adjacent node
                    adjNode = locationDict[road.startID]

                    # calculate adjacent distance using sphere calc
                    adjDist = (distance_on_unit_sphere(node.lat, node.long, adjNode.lat, adjNode.long)) * 3960
                    # convert to time and add to previous g
                    g = node.g + (adjDist / float(road.speedLimit))

                    # calculate h based on goal node
                    hDist = (distance_on_unit_sphere(adjNode.lat, adjNode.long, goalLocation.lat, goalLocation.long)) * 3960
                    h = hDist / 65

                    f = g + h

                    # if adjacent node not in priority queue
                    if adjNode.ID not in frontier.entry_finder:
                        frontier.push(adjNode.ID, f)
                        # update adjacent node object's features
                        adjNode.set_parent(node.ID)
                        adjNode.update_g(g)
                        adjNode.update_h(h)
                        adjNode.update_f(f)

                        # debug option
                        if DEBUG:
                            print("\tAdding {}, g={}, h={}, f={} to the frontier.".format(adjNode.ID, adjNode.g * 60,
                                                                                         adjNode.h * 60, adjNode.f * 60))

                    # if adjacent node's f is less than its current f in priority queue
                    elif f < frontier.entry_finder[adjNode.ID][0]:
                        # debug options
                        if DEBUG:
                            print("\tUpdating path cost for {} on the frontier.".format(adjNode.ID))
                            print("\t\told: g={}, h={}, f={}".format(adjNode.g * 60, adjNode.h * 60, adjNode.f * 60))

                        frontier.push(adjNode.ID, f)
                        # update adjacent node object's features
                        adjNode.set_parent(node.ID)
                        adjNode.update_g(g)
                        adjNode.update_h(h)
                        adjNode.update_f(f)

                        # debug option
                        if DEBUG:
                            print("\t\tnew: g={}, h={}, f={}".format(adjNode.g * 60, adjNode.h * 60, adjNode.f * 60))

                    else:
                        # if adjacent node's f is more than its current f in priority queue
                        continue
                else:
                    # node is already explored
                    continue

        explored.append(nodeID)
        # debug options
        if DEBUG:
            print()

    return locationDict, expanded_count

def back_track(locationDict, startID, goalID):
    resultList = []

    resultList += [locationDict[goalID].ID]
    parent = locationDict[goalID].parent
    resultList += [parent]

    while parent != startID:
        parent = locationDict[parent].parent
        resultList += [parent]

    return resultList



def main():
    # retrieve filename from user
    mapfile = str(input("Please enter a map filename: "))

    # parse input file
    locationDict, roadDict = parse_map(mapfile)

    # retrieve start and goal location IDs
    startID = input("Please enter the ID for the starting location: ")
    goalID = input("Please enter the ID for the goal location: ")

    print("\nRouting from {} to {}\n".format(startID, goalID))

    # run A*
    updatedLocationDict, expanded_count = a_star(locationDict, roadDict, startID, goalID)

    # debug options
    if DEBUG:
        print("\n")

    # backtrack final path found into list
    results = back_track(updatedLocationDict, startID, goalID)

    print("Total travel time is {} minutes".format(updatedLocationDict[goalID].f * 60))
    print("Number of nodes expanded: {}".format(expanded_count - 1))
    print("Path found is:")

    for location in reversed(results):
        if location == startID:
            print(location, " (starting location)")
            previous = location
        else:
            roadList = roadDict[location]
            for road in roadList:
                if previous == road.startID or previous == road.endID:
                    print(location, " ", road.name)
            previous = location



    return 0


if __name__ == "__main__":
    main()
