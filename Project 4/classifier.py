from itertools import islice


def txtCheck(filename):
    if filename[-4:] != ".txt":
        filename += ".txt"
    return filename

def parseEmail(word_list):
    word_dict = {}
    email_count = 0
    start_indx = [i for i, v in enumerate(word_list) if v == "<SUBJECT>"]
    end_indx = [i for i, v in enumerate(word_list) if v == "</BODY>"]
    comb_indx = [(start_indx[i] + 1, end_indx[i]) for i in range(len(start_indx))]
    email_list = [list(islice(word_list, a, b)) for a, b in comb_indx]
    for i in range(len(email_list)):
        email_list[i] = list(filter(lambda a: a != "</SUBJECT>" and a != "<BODY>", email_list[i]))
    for item in email_list:
        temp = set()
        # print(item)
        gen = (line.split() for line in item if len(line) > 0)
        for line in gen:
            print(line)
            for word in line:
                temp.add(word.lower())
        print(list(temp))
        print()


    return word_dict, email_count

class Classifier:
    def __init__(self, file_list):
        self.spam_train_file, self.ham_train_file, self.spam_test_file, self.ham_test_file = file_list

        self.train()

    def train(self):
        spam_list = open(txtCheck(self.spam_train_file), "r").read().splitlines()
        spam_dict, email_count_spamt = parseEmail(spam_list)
        # print(spam_dict)
        # print(email_count_spamt)

        # ham_list = open(txtCheck(self.ham_train_file), "r").read().splitlines()
        # ham_dict, email_count_hamt = parseEmail(ham_list)
        # print(ham_dict)
        # print(email_count_hamt)
