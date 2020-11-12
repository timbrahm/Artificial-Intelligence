import numpy as np

def txtCheck(filename):
    if filename[-4:] != ".txt":
        filename += ".txt"
    return filename

class Classifier:
    def __init__(self, file_list, DEBUG):
        self.DEBUG = DEBUG

        self.spam_train_file, self.ham_train_file, self.spam_test_file, self.ham_test_file = file_list

        self.spam_dict, self.email_count_spam_train, self.ham_dict, self.email_count_ham_train = self.train()

        self.Pspam = self.email_count_spam_train / (self.email_count_spam_train + self.email_count_ham_train)
        self.Pham = self.email_count_ham_train / (self.email_count_spam_train + self.email_count_ham_train)

        self.feat_given_spam, self.feat_given_ham = self.featureProbs()

    def train(self):
        spam_dict = {}
        email_count_spam_train = 0
        with open(txtCheck(self.spam_train_file), "r") as file:
            email_set = set()
            for line in file:
                line = line.rstrip()
                if line == "<SUBJECT>":
                    email_count_spam_train += 1
                    email_set = set()
                elif line == "</BODY>":
                    email_list = list(email_set)
                    for word in email_list:
                        word = word.lower()
                        spam_dict[word] = spam_dict.get(word, 0) + 1
                elif line != "</SUBJECT>" and line != "<BODY>" and line != "":
                    line = line.split()
                    for word in line:
                        word = word.lower()
                        email_set.add(word)
            file.close()

        ham_dict = dict.fromkeys(spam_dict, 0)
        email_count_ham_train = 0
        with open(txtCheck(self.ham_train_file), "r") as file:
            email_set = set()
            for line in file:
                line = line.rstrip()
                if line == "<SUBJECT>":
                    email_count_ham_train += 1
                    email_set = set()
                elif line == "</BODY>":
                    email_list = list(email_set)
                    for word in email_list:
                        word = word.lower()
                        try:
                            ham_dict[word] += 1
                        except KeyError:
                            ham_dict[word] = 1
                            spam_dict[word] = 0
                elif line != "</SUBJECT>" and line != "<BODY>" and line != "":
                    line = line.split()
                    for word in line:
                        word = word.lower()
                        email_set.add(word)
            file.close()
        return spam_dict, email_count_spam_train, ham_dict, email_count_ham_train

    def featureProbs(self):
        feat_given_spam = {}
        feat_given_ham = {}
        for feature in self.spam_dict:
            feat_given_spam[feature] = (self.spam_dict[feature] + 1) / (self.email_count_spam_train + 2)
        for feature in self.ham_dict:
            feat_given_ham[feature] = (self.ham_dict[feature] + 1) / (self.email_count_ham_train + 2)
        return feat_given_spam, feat_given_ham

    def test(self, type_check):
        if type_check == "SPAM":
            email_count_spam_test = 0
            correct_spam_count = 0
            with open(txtCheck(self.spam_test_file), "r") as file:
                feat_dict = {}
                for line in file:
                    line = line.rstrip()
                    if line == "<SUBJECT>":
                        email_count_spam_test += 1

                        if self.DEBUG:
                            print("Test email {}".format(email_count_spam_test))
                            print("priors= {} {}".format(self.Pspam, self.Pham))

                        feat_dict = dict.fromkeys(self.spam_dict, False)
                    elif line == "</BODY>":
                        ##For SPAM
                        total_spam_prob = self.Pspam
                        total_spam_prob_log = np.log(self.Pspam)
                        for feat in feat_dict:
                            feat_prob = self.feat_given_spam[feat]
                            if not feat_dict[feat]:
                                feat_prob = 1 - feat_prob
                            total_spam_prob *= feat_prob
                            total_spam_prob_log += np.log(feat_prob)
                            if feat_prob <= 0:
                                print("WARNING: {}".format(feat_prob))

                        ##For HAM
                        total_ham_prob = self.Pham
                        total_ham_prob_log = np.log(self.Pham)
                        for feat in feat_dict:
                            feat_prob = self.feat_given_ham[feat]
                            if not feat_dict[feat]:
                                feat_prob = 1 - feat_prob
                            total_ham_prob *= feat_prob
                            total_ham_prob_log += np.log(feat_prob)


                        if self.DEBUG:
                            print("probs= {:.4f} {:.4f}".format(total_spam_prob, total_ham_prob))

                        if total_spam_prob_log > total_ham_prob_log:
                            spam_class = "SPAM"
                            correct = "right"
                            correct_spam_count += 1
                        else:
                            spam_class = "HAM"
                            correct = "wrong"
                        true_count = sum(feat_dict.values())
                        print("TEST {} {}/{} features true {:.3f} {:.3f} {} {}".format(email_count_spam_test, true_count, len(feat_dict), total_spam_prob_log, total_ham_prob_log, spam_class.lower(), correct))

                    elif line != "</SUBJECT>" and line != "<BODY>" and line != "":
                        line = line.split()
                        for word in line:
                            word = word.lower()
                            if word in feat_dict:
                                feat_dict[word] = True
                file.close()
            return correct_spam_count, email_count_spam_test
        else:
            email_count_ham_test = 0
            correct_ham_count = 0
            with open(txtCheck(self.ham_test_file), "r") as file:
                feat_dict = {}
                for line in file:
                    line = line.rstrip()
                    if line == "<SUBJECT>":
                        email_count_ham_test += 1

                        if self.DEBUG:
                            print("Test email {}".format(email_count_ham_test))
                            print("priors= {} {}".format(self.Pspam, self.Pham))

                        feat_dict = dict.fromkeys(self.spam_dict, False)
                    elif line == "</BODY>":
                        ##For SPAM
                        total_spam_prob = self.Pspam
                        total_spam_prob_log = np.log(self.Pspam)
                        for feat in feat_dict:
                            feat_prob = self.feat_given_spam[feat]
                            if not feat_dict[feat]:
                                feat_prob = 1 - feat_prob
                            total_spam_prob *= feat_prob
                            total_spam_prob_log += np.log(feat_prob)

                        ##For HAM
                        total_ham_prob = self.Pham
                        total_ham_prob_log = np.log(self.Pham)
                        for feat in feat_dict:
                            feat_prob = self.feat_given_ham[feat]
                            if not feat_dict[feat]:
                                feat_prob = 1 - feat_prob
                            total_ham_prob *= feat_prob
                            total_ham_prob_log += np.log(feat_prob)

                        if self.DEBUG:
                            print("probs= {:.4f} {:.4f}".format(total_spam_prob, total_ham_prob))

                        if total_spam_prob_log > total_ham_prob_log:
                            spam_class = "SPAM"
                            correct = "wrong"
                        else:
                            spam_class = "HAM"
                            correct = "right"
                            correct_ham_count += 1
                        true_count = sum(feat_dict.values())
                        print("TEST {} {}/{} features true {:.3f} {:.3f} {} {}".format(email_count_ham_test, true_count,
                                                                                       len(feat_dict), total_spam_prob_log,
                                                                                       total_ham_prob_log,
                                                                                       spam_class.lower(), correct))

                    elif line != "</SUBJECT>" and line != "<BODY>" and len(line) > 0:
                        line = line.split()
                        for word in line:
                            word = word.lower()
                            if word in feat_dict:
                                feat_dict[word] = True
                file.close()
            return correct_ham_count, email_count_ham_test
