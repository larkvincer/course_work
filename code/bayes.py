from collections import Counter, defaultdict
import math
import random
import re
import glob

def create_tokens(message):
    # convert to lower case
    message = message.lower()                    
    # split words
    all_words = re.findall("[a-z0-9']+", message)
    # select only unque words
    return set(all_words) 

def count_words(training_set):
    # create dctionary with default factory [0, 0]
    counts = defaultdict(lambda: [0, 0])
    # terate though set and count how many times words appears
    #n both spam and non-spam
    for message, is_spam in training_set:
        for word in create_tokens(message):
            counts[word][0 if is_spam else 1] += 1
    # return dct with words and
    # lst [spam_counter, nonspam_counter]
    return counts

def word_probablities(counts, total_spams, total_non_spams, k=0.5):
    # create a trples from word_counts dict
    # w, p(w | spam) and p(w | nonspam)
    return [(w,
             (spam + k) / (total_spams + 2 * k),
             (non_spam + k) / (total_non_spams + 2 * k))
             for w, (spam, non_spam) in counts.items()] 

def spam_probability(probs_for_word, message):
    # get unque tokens
    message_words = create_tokens(message)
    # logorphmic probabilities from message
    log_prob_if_spam = log_prob_if_not_spam = 0.0

    for word, prob_if_spam, prob_if_not_spam in probs_for_word:

        # for each word n the message,
        # add the log probablity of seeing it
        if word in message_words:
            log_prob_if_spam += math.log(prob_if_spam)
            log_prob_if_not_spam += math.log(prob_if_not_spam)

        # for each word that's not n the message
        # add the log probablity of _not_ seeing it
        else:
            log_prob_if_spam += math.log(1.0 - prob_if_spam)
            log_prob_if_not_spam += math.log(1.0 - prob_if_not_spam)

    # get rid of logoriphm
    prob_if_spam = math.exp(log_prob_if_spam)
    prob_if_not_spam = math.exp(log_prob_if_not_spam)

    return prob_if_spam / (prob_if_spam + prob_if_not_spam)


class BayesClassifier:

    def __init__(self, k=0.5):
        # pseudo counter to avod 0 probability
        self.k = k
        self.probs_for_word = [] 

    def train(self, training_set):

        # count spam and non-spam messages
        num_spams = len([is_spam
                         for message, is_spam in training_set
                         if is_spam])
        num_non_spams = len(training_set) - num_spams

        # counts how many each word appears in spam and nonspam
        word_counts = count_words(training_set)

        # calculate probablites for each word
        self.probs_for_word = word_probablities(word_counts,
                                             num_spams,
                                             num_non_spams,
                                             self.k)

    def create_classification(self, message):
        return spam_probability(self.probs_for_word, message)

# using only subject part of message for symplicity
def get_subject_data(path):

    data = []

    # regex for stripping out the leading "Subject:" and any spaces after it
    subject_regex = re.compile(r"^Subject:\s+")

    # iterate through each file appears in path
    for fn in glob.glob(path):
        # check if iteration are performed on spam or on ham
        is_spam = "ham" not in fn

        with open(fn,'r') as file:
            for line in file:
                if line.startswith("Subject:"):
                    subject = subject_regex.sub("", line).strip()
                    data.append((subject, is_spam))

    return data

def split_data(data, prob):
    # create fractions [prob, 1 - prob]
    # store
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results

def p_spam_given_word(word_prob):
    word, prob_if_spam, prob_if_not_spam = word_prob
    return prob_if_spam / (prob_if_spam + prob_if_not_spam)


def train_and_test_model(path):

    data = get_subject_data(path)
    train_data, test_data = split_data(data, 0.75)

    classifier = BayesClassifier()
    classifier.train(train_data)

    classified = [(subject, is_spam, classifier.create_classification(subject))
              for subject, is_spam in test_data]

    counts = Counter((is_spam, spam_probability > 0.5)
                     for _, is_spam, spam_probability in classified)

    print(counts)

    classified.sort(key=lambda row: row[2])
    spammiest_hams = list(filter(lambda row: not row[1], classified))[-5:]
    hammiest_spams = list(filter(lambda row: row[1], classified))[:5]

    print("spammiest_hams", spammiest_hams)
    print("hammiest_spams", hammiest_spams)

    words = sorted(classifier.probs_for_word, key=p_spam_given_word)

    spammiest_words = words[-5:]
    hammiest_words = words[:5]

    print("spammiest_words", spammiest_words)
    print("hammiest_words", hammiest_words)


if __name__ == "__main__":
    train_and_test_model(r"/home/larkvincer/Documents/course_work/code/src/*/*")
