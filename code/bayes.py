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
    # select only unique words
    return set(all_words) 

def count_words(training_set):
    # create dictionary with default factory [0, 0]
    counts = defaultdict(lambda: [0, 0])
    # iterate though set and count how many times words appears
    #in both spam and non-spam
    for message, is_spam in training_set:
        for word in create_tokens(message):
            counts[word][0 if is_spam else 1] += 1
    # return dict with words and
    # list [spam_counter, nonspam_counter]
    return counts

def word_probabilities(counts, total_spams, total_non_spams, k=0.5):
    # create a triples from word_counts dict
    # w, p(w | spam) and p(w | nonspam)
    return [(w,
             (spam + k) / (total_spams + 2 * k),
             (non_spam + k) / (total_non_spams + 2 * k))
             for w, (spam, non_spam) in counts.items()] 

def spam_probability(word_probs, message):
    # get unique tokens
    message_words = create_tokens(message)
    # logoriphmic probabilities from message
    log_prob_if_spam = log_prob_if_not_spam = 0.0

    for word, prob_if_spam, prob_if_not_spam in word_probs:

        # for each word in the message,
        # add the log probability of seeing it
        if word in message_words:
            log_prob_if_spam += math.log(prob_if_spam)
            log_prob_if_not_spam += math.log(prob_if_not_spam)

        # for each word that's not in the message
        # add the log probability of _not_ seeing it
        else:
            log_prob_if_spam += math.log(1.0 - prob_if_spam)
            log_prob_if_not_spam += math.log(1.0 - prob_if_not_spam)

    # get rid of logoriphm
    prob_if_spam = math.exp(log_prob_if_spam)
    prob_if_not_spam = math.exp(log_prob_if_not_spam)

    return prob_if_spam / (prob_if_spam + prob_if_not_spam)
