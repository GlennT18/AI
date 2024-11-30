from math import log10
from typing import List

class NaiveBayes:
    def __init__(self):
        #vars
        self.vocab = set()
        self.word_prob_spam = {}
        self.word_prob_ham = {}
        self.p_spam = 0
        self.p_ham = 0

    def train(self, spams: List[List[str]], hams: List[List[str]]) -> None:
        #number of spams, hams, and emails
        num_spams = len(spams)
        num_hams = len(hams)
        total_emails = num_spams + num_hams

        #calculating priors
        self.p_spam = num_spams / total_emails
        self.p_ham = num_hams / total_emails

        #keep track of works and the amount of them
        spam_word_counts = {}
        ham_word_counts = {}
        total_spam_words = 0
        total_ham_words = 0

        #going through each email in spams list
        for email in spams:
            for word in email:
                #adding the word to vocab list, dictionary, and incrementing
                self.vocab.add(word)
                spam_word_counts[word] = spam_word_counts.get(word, 0) + 1
                total_spam_words += 1

        #going through each email in hams list
        for email in hams:
            for word in email:
                #adding the word to vocab list, dictionary, and incrementing
                self.vocab.add(word)
                ham_word_counts[word] = ham_word_counts.get(word, 0) + 1
                total_ham_words += 1

        #finding probability with additive smoothening
        #(number of times the word has been seen + 1) / (amount of spam(ham) woreds + total words)
        vocab_size = len(self.vocab)
        for word in self.vocab:
            self.word_prob_spam[word] = (spam_word_counts.get(word, 0) + 1) / (total_spam_words + vocab_size)
            self.word_prob_ham[word] = (ham_word_counts.get(word, 0) + 1) / (total_ham_words + vocab_size)


    def predict_is_spam(self, email: List[str]) -> bool:
        #log the probabilities
        log_p_spam = log10(self.p_spam)
        log_p_ham = log10(self.p_ham)

        #go through the email
        for word in email:
            if word in self.vocab:
                #if the word is in our vocab, updatge p(S) and p(H)
                log_p_spam += log10(self.word_prob_spam.get(word, 1e-10))
                log_p_ham += log10(self.word_prob_ham.get(word, 1e-10))

        return log_p_spam > log_p_ham
