from classifier import Classifier


def main():
    # spam_train_file = input("Please enter a training file for spam: ")
    # ham_train_file = input("Please enter a training file for ham: ")
    # spam_test_file = input("Please enter a testing file for spam: ")
    # ham_test_file = input("Please enter a testing file for ham: ")
    spam_train_file = "train-spam-small.txt"
    ham_train_file = "train-ham-small.txt"
    spam_test_file = "test-spam-small.txt"
    ham_test_file = "test-ham-small.txt"
    file_list = [spam_train_file, ham_train_file, spam_test_file, ham_test_file]

    spam_classifier = Classifier(file_list)

    return 0


if __name__ == "__main__":
    main()
