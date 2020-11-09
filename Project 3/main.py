from decimal import *

from lastLocation import LastLocation
from currentLocation import CurrentLocation
from motionSensor import MotionSensor
from soundSensor import SoundSensor

DEBUG = False       #toggle DEBUG messaging
DIGITS = Decimal(10) ** -8      #quantize probabilities to 8 places in decimal library


def main():
    #user input
    input_file = input("Please enter a txt file to open: ")
    if input_file[-4:] != ".txt":
        input_file += ".txt"

    #parse input file
    text_list = open(input_file, "r").read().splitlines()
    text_list = [i.split() for i in text_list]
    m, n = int(text_list[0][0]), int(text_list[0][1])
    time_steps = text_list[1:]

    #initialize random variable objects
    last = LastLocation(m, n)
    curr = CurrentLocation(m, n)
    motion = MotionSensor(m, n)
    sound = SoundSensor(m, n)

    #DEBUG messages
    if DEBUG:
        print("Last location distribution:")
        for loc in last.CPT:
            print("Last location: {}, prob: {}".format(loc, last.CPT[loc].quantize(DIGITS)))

        print("\nCurrent location distribution:")
        for loc in last.CPT:
            print("Last location: {}".format(loc))
            loc_distrib = curr.getDistrib(loc)
            for curr_loc in loc_distrib[1]:
                if loc_distrib[1][curr_loc] != 0:
                    print("\tCurrent location: {}, prob: {}".format(curr_loc, loc_distrib[1][curr_loc].quantize(DIGITS)))

        print("\nMotion sensor #1 (top left) distribution:")
        for loc in motion.m1CPT:
            print("Current location: {}, true prob: {}, false prob: {}".format(loc,
                                                                               motion.m1CPT[loc][True].quantize(DIGITS),
                                                                               motion.m1CPT[loc][False].quantize(DIGITS)))
        print("\nMotion sensor #2 (bottom right) distribution:")
        for loc in motion.m2CPT:
            print("Current location: {}, true prob: {}, false prob: {}".format(loc,
                                                                               motion.m2CPT[loc][True].quantize(DIGITS),
                                                                               motion.m2CPT[loc][False].quantize(DIGITS)))

        print("\nSound distribution:")
        for curr_loc in sound.CPT:
            print("Current location: {}".format(curr_loc))
            for loc in sound.CPT[curr_loc]:
                print("\tSound reported at: {}, prob: {}".format(loc, sound.CPT[curr_loc][loc].quantize(DIGITS)))
        print()


    #initial distribution
    print("Initial distribution of monkey's last location:")
    for i in range(m):
        print("\t", end="")
        for j in range(n):
            print("{}".format(last.CPT[(i, j)].quantize(DIGITS)), end=" ")
        print()

    #subsequent time steps
    for time_step in time_steps:
        M1 = True if int(time_step[0]) == 1 else False
        M2 = True if int(time_step[1]) == 1 else False
        S = (int(time_step[2]), int(time_step[3]))
        print("\nObservation: Motion1: {}, Motion2: {}, Sound location: {}".format(bool(M1), bool(M2), S))
        print("Monkey's predicted current location at time step: {}".format(last.time_step))

        #calculate probabilities from sum
        prob_dict = {}
        for curr_loc in curr.CPT:
            prob_dict[curr_loc] = Decimal(0)
            for loc in last.CPT:
                prob_dict[curr_loc] += Decimal(last.CPT[loc] * curr.CPT[loc][curr_loc] * motion.m1CPT[curr_loc][M1] *
                                        motion.m2CPT[curr_loc][M2] * sound.CPT[curr_loc][S])

        #DEBUG messaging
        if DEBUG:
            for curr_loc in curr.CPT:
                print("\tCalculating total prob for current location: {}".format(curr_loc))
                for loc in last.CPT:
                    print("\t\tProbs being multiplied for last location {}: {} {} {} {} {}".format(loc, last.CPT[loc],
                          curr.CPT[loc][curr_loc], motion.m1CPT[curr_loc][M1], motion.m2CPT[curr_loc][M2], sound.CPT[curr_loc][S]))
            print("\nBefore normalization:")
            for i in range(m):
                print("\t", end="")
                for j in range(n):
                    print("{:.8f}".format(prob_dict[(i, j)].quantize(DIGITS)), end=" ")
                print()
            print()
            print("After normalization:")


        #normalize values
        prob_sum = sum(prob_dict.values())
        prob_dict = {k: v / prob_sum for k, v in prob_dict.items()}

        for i in range(m):
            print("\t", end="")
            for j in range(n):
                print("{:.8f}".format(prob_dict[(i, j)].quantize(DIGITS)), end=" ")
            print()

        #update last CPT with current and update time step
        last.updateCPT(prob_dict)
        last.updateTime(last.time_step + 1)

    return 0


if __name__ == "__main__":
    main()
