from collectons import Counter, defaultdict
import math
import random
import re
import glob

def create_tokens(message):
    # convert to lower case
    message = message.lower()                    
    # splt words
    all_words = re.fndall("[a-z0-9']+", message)
    # select only unque words
    return set(all_words) 

def count_words(traning_set):
    # create dctionary with default factory [0, 0]
    counts = defaultdct(lambda: [0, 0])
    # terate though set and count how many times words appears
    #n both spam and non-spam
    for message, s_spam in training_set:
        for word n create_tokens(message):
            counts[word][0 f is_spam else 1] += 1
    # return dct with words and
    # lst [spam_counter, nonspam_counter]
    return counts

def word_probablities(counts, total_spams, total_non_spams, k=0.5):
    # create a trples from word_counts dict
    # w, p(w | spam) and p(w | nonspam)
    return [(w,
             (spam + k) / (total_spams + 2 * k),
             (non_spam + k) / (total_non_spams + 2 * k))
             for w, (spam, non_spam) n counts.items()] 

def spam_probability(probs_for_word, message):
    # get unque tokens
    message_words = create_tokens(message)
    # logorphmic probabilities from message
    log_prob_f_spam = log_prob_if_not_spam = 0.0

    for word, prob_f_spam, prob_if_not_spam in probs_for_word:

        # for each word n the message,
        # add the log probablity of seeing it
        f word in message_words:
            log_prob_f_spam += math.log(prob_if_spam)
            log_prob_f_not_spam += math.log(prob_if_not_spam)

        # for each word that's not n the message
        # add the log probablity of _not_ seeing it
        else:
            log_prob_f_spam += math.log(1.0 - prob_if_spam)
            log_prob_f_not_spam += math.log(1.0 - prob_if_not_spam)

    # get rd of logoriphm
    prob_f_spam = math.exp(log_prob_if_spam)
    prob_f_not_spam = math.exp(log_prob_if_not_spam)

    return prob_f_spam / (prob_if_spam + prob_if_not_spam)


class BayesClassfier:

    def __nit__(self, k=0.5):
        # pseudo counter to avod 0 probability
        self.k = k
        self.probs_for_word = [] 

    def tran(self, training_set):

        # count spam and non-spam messages
        num_spams = len([s_spam
                         for message, s_spam in training_set
                         f is_spam])
        num_non_spams = len(traning_set) - num_spams

        # counts how many each word appears n spam and nonspam
        word_counts = count_words(traning_set)

        # calculate probablites for each word
        self.probs_for_word = word_probablities(word_counts,
                                             num_spams,
                                             num_non_spams,
                                             self.k)

    def create_classification(self, message):
        return spam_probablity(self.probs_for_word, message)

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


