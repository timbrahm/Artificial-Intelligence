import numpy as np

## function that appends txt file extension on input filename if it doesn't have it
def txtCheck(filename):
    if filename[-4:] != ".txt":
        filename += ".txt"
    return filename

class Classifier:
    def __init__(self, file_list, DEBUG):
        ## keep debug constants consistent
        self.DEBUG = DEBUG

        ## input files from main
        self.spam_train_file, self.ham_train_file, self.spam_test_file, self.ham_test_file = file_list

        ## vocab dicts and email count numbers
        self.spam_dict, self.email_count_spam_train, self.ham_dict, self.email_count_ham_train = self.train()

        ## priors
        self.Pspam = self.email_count_spam_train / (self.email_count_spam_train + self.email_count_ham_train)
        self.Pham = self.email_count_ham_train / (self.email_count_spam_train + self.email_count_ham_train)

        ## feat probs
        self.feat_given_spam, self.feat_given_ham = self.featureProbs()

    ## Train input from spam and ham input files
    def train(self):
        spam_dict = {}
        email_count_spam_train = 0
        ## open spam training file
        with open(txtCheck(self.spam_train_file), "r") as file:
            ## use set to only consider each word once per email
            email_set = set()
            for line in file:
                line = line.rstrip()
                ## start of new email
                if line == "<SUBJECT>":
                    email_count_spam_train += 1
                    email_set = set()
                ## end of email
                elif line == "</BODY>":
                    email_list = list(email_set)
                    ## add words to vocab list
                    for word in email_list:
                        word = word.lower()
                        spam_dict[word] = spam_dict.get(word, 0) + 1
                ## any line other than beginning or end of email
                elif line != "</SUBJECT>" and line != "<BODY>" and line != "":
                    line = line.split()
                    for word in line:
                        word = word.lower()
                        email_set.add(word)
            file.close()

        ham_dict = dict.fromkeys(spam_dict, 0)
        email_count_ham_train = 0
        ## open ham training file
        with open(txtCheck(self.ham_train_file), "r") as file:
            ## use set again to count words once per email
            email_set = set()
            for line in file:
                line = line.rstrip()
                ## start new email
                if line == "<SUBJECT>":
                    email_count_ham_train += 1
                    email_set = set()
                ## end email
                elif line == "</BODY>":
                    email_list = list(email_set)
                    for word in email_list:
                        word = word.lower()
                        ## if word existed in spam dict
                        try:
                            ham_dict[word] += 1
                        ## if it's a new word
                        except KeyError:
                            ham_dict[word] = 1
                            spam_dict[word] = 0
                ## any other line but start or end lines
                elif line != "</SUBJECT>" and line != "<BODY>" and line != "":
                    line = line.split()
                    for word in line:
                        word = word.lower()
                        email_set.add(word)
            file.close()
        return spam_dict, email_count_spam_train, ham_dict, email_count_ham_train

    ## calculate feature probabilities for all features given both spam and given ham
    def featureProbs(self):
        feat_given_spam = {}
        feat_given_ham = {}
        for feature in self.spam_dict:
            feat_given_spam[feature] = (self.spam_dict[feature] + 1) / (self.email_count_spam_train + 2)
        for feature in self.ham_dict:
            feat_given_ham[feature] = (self.ham_dict[feature] + 1) / (self.email_count_ham_train + 2)
        return feat_given_spam, feat_given_ham

    ## test the input testing files for spam and ham
    def test(self, type_check):
        ## need distinct func calls in main
        if type_check == "SPAM":
            email_count_spam_test = 0
            correct_spam_count = 0
            ## open spam testing file
            with open(txtCheck(self.spam_test_file), "r") as file:
                feat_dict = {}
                for line in file:
                    line = line.rstrip()
                    ## new email line
                    if line == "<SUBJECT>":
                        email_count_spam_test += 1

                        if self.DEBUG:
                            print("Test email {}".format(email_count_spam_test))
                            print("priors= {} {}".format(self.Pspam, self.Pham))

                        feat_dict = dict.fromkeys(self.spam_dict, False)
                    ## endline for email
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

                    ## any other line but start and end lines
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
            ## open ham testing file
            with open(txtCheck(self.ham_test_file), "r") as file:
                feat_dict = {}
                for line in file:
                    line = line.rstrip()
                    ## new email line
                    if line == "<SUBJECT>":
                        email_count_ham_test += 1

                        if self.DEBUG:
                            print("Test email {}".format(email_count_ham_test))
                            print("priors= {} {}".format(self.Pspam, self.Pham))

                        feat_dict = dict.fromkeys(self.spam_dict, False)
                    ## end email line
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

                    ## any other line but start or end lines
                    elif line != "</SUBJECT>" and line != "<BODY>" and len(line) > 0:
                        line = line.split()
                        for word in line:
                            word = word.lower()
                            if word in feat_dict:
                                feat_dict[word] = True
                file.close()
            return correct_ham_count, email_count_ham_test
