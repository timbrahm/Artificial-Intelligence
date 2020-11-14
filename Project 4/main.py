from classifier import Classifier


DEBUG = False

def main():
    spam_train_file = input("Please enter a training file for spam: ")
    ham_train_file = input("Please enter a training file for ham: ")
    spam_test_file = input("Please enter a testing file for spam: ")
    ham_test_file = input("Please enter a testing file for ham: ")


    file_list = [spam_train_file, ham_train_file, spam_test_file, ham_test_file]

    spam_classifier = Classifier(file_list, DEBUG)

    if DEBUG:
        print("Training from {} and {}".format(spam_train_file, ham_train_file))
        print("Testing from {} and {}".format(spam_test_file, ham_test_file))
        print("number of emails: {} vs {}".format(spam_classifier.email_count_spam_train, spam_classifier.email_count_ham_train))
        print("entire vocab: {}".format(list(spam_classifier.spam_dict.keys())))
        print("entire vocab size is: {}".format(len(spam_classifier.spam_dict.keys())))
        print("spam words: {}".format(spam_classifier.spam_dict))
        print("ham words: {}".format(spam_classifier.ham_dict))
        print("Beginning tests.")
        print("Testing spam emails.")

    correct_spam, total_spam = spam_classifier.test("SPAM")

    if DEBUG:
        print("{} out of {} classified correctly.".format(correct_spam, total_spam))

        print("Testing ham emails.")

    correct_ham, total_ham = spam_classifier.test("HAM")

    if DEBUG:
        print("{} out of {} classified correctly.".format(correct_ham, total_ham))

    correct = correct_spam + correct_ham
    total = total_spam + total_ham
    print("Total: {}/{} emails classified correctly.".format(correct, total))

    return 0


if __name__ == "__main__":
    main()
