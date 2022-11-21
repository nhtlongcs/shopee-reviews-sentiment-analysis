import numpy as np
import os
from typing import Dict, List


MAX_VAL = np.iinfo(np.int32).max


def split_phrase_to_words(phrase, word_dict, max_word_len=10):
    len_phrase = len(phrase)
    dp = np.full(len_phrase + 1, MAX_VAL)
    trade = np.zeros(len_phrase + 1, dtype='int')
    for ind in range(0, len(phrase)):
        for wlen in range(1, max_word_len + 1):
            if (wlen > ind + 1):
                break
            subseq = phrase[ind - wlen + 1: ind + 1]
            if (subseq in word_dict):
                if (ind - wlen == -1):
                    dp[ind] = 1
                    trade[ind] = wlen
                elif (dp[ind] > dp[ind - wlen] + 1):
                    dp[ind] = dp[ind - wlen] + 1
                    trade[ind] = wlen

    if dp[len_phrase - 1] != MAX_VAL:
        ind = len_phrase - 1
        words = []
        while ind >= 0:
            wlen = trade[ind]
            w = phrase[ind - wlen + 1: ind + 1]
            words.append(w)
            ind -= wlen
        words.reverse()
        return words
    else:
        return None


if __name__ == '__main__':

    DICT_PATH = os.path.join(os.getcwd(), 'dicts/vi.txt')

    word_dict = {}
    f = open(DICT_PATH, 'r')
    lines = f.readlines()
    for l in lines:
        l = l.strip().upper()
        word_dict[l] = True
    phrase = 'HÀNI'
    words = split_phrase_to_words(phrase, word_dict=word_dict)
    print(words)
