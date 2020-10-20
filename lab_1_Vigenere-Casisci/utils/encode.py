import math
import re
from collections import Counter

from functools import reduce

import numpy as np


def find_gcd(array):
    x = reduce(math.gcd, array)
    return x


def gram_gcd(positions):
    distances = []
    for j in range(1, len(positions)):
        distances.append(positions[j] - positions[j - 1])
    # filtering random grams
    frequency = Counter(distances)
    leave_num = math.ceil(0.9 * len(frequency))  # change threshold
    frequency = frequency.most_common(leave_num)
    distances = [f[0] for f in frequency]
    # end
    gcd = find_gcd(distances)
    return gcd


def add_gsd(gcd_array, gcd):
    if gcd > 1:
        gcd_array.append(gcd)


def casisci(text):
    text_length = len(text)
    text = text.lower()
    gcd_array = []
    grams = {}
    for i in range(text_length - 1):
        search = text[i: i + 2]
        if grams.get(search) is None:
            positions = [token.start() for token in re.finditer(search, text)]
            if len(positions) > 2:  # or 1
                grams[search] = positions
                add_gsd(gcd_array, gram_gcd(positions))
    i = 0
    while i < len(grams.keys()):
        gram = list(grams.keys())[i]
        for pos in grams[gram]:
            search = text[pos: pos + len(gram) + 1]
            if grams.get(search) is None:
                positions = [token.start() for token in re.finditer(search, text)]
                if len(positions) > 2:  # or 1
                    grams[search] = positions
                    add_gsd(gcd_array, gram_gcd(positions))
        i += 1
    answer = max(set(gcd_array), key=gcd_array.count)
    return answer


def get_text_frequencies(text, eng_frequencies):
    alphabet = list(map(lambda x: x['letter'], eng_frequencies))
    letters_repeat = dict.fromkeys(alphabet, 0.0)
    for letter in text:
        if letters_repeat.get(letter.lower()) is not None:
            letters_repeat[letter.lower()] += 1
    letters_num = sum(letters_repeat.values())
    letters_num = letters_num if letters_num > 0 else 1
    for letter in letters_repeat:
        letters_repeat[letter] = letters_repeat[letter] / letters_num
    return letters_repeat


def find_key_shift(text, eng_frequencies):
    alphabet_frequencies = eng_frequencies
    text_frequencies = get_text_frequencies(text, eng_frequencies)
    shifts = {}
    for i in range(len(alphabet_frequencies)):
        absolute_val_array = np.abs(np.array(list(text_frequencies.values())) - alphabet_frequencies[i]['frequency'])
        smallest_difference_index = absolute_val_array.argmin()
        shifts[smallest_difference_index - i] = shifts.get(smallest_difference_index - i, 0) + 1
    max_num_shifts = max(shifts, key=lambda x: shifts[x])
    return max_num_shifts if max_num_shifts >= 0 else len(eng_frequencies) + max_num_shifts
