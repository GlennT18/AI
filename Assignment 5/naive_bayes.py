from math import log10
from typing import List


class NaiveBayes:
    def __init__(self):
        # You may add fields you need here
        pass

    def train(self, spams: List[List[str]], hams: List[List[str]]) -> None:
        raise NotImplementedError  # TODO: Replace this line with your code

    def predict_is_spam(self, email: List[str]) -> bool:
        raise NotImplementedError  # TODO: Replace this line with your code
