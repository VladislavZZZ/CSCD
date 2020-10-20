import random
import matplotlib.pyplot as plt
import numpy as np
from utils import decode,encode,file_funcsc
import argparse

eng_frequencies = [
    {"letter": "a", "frequency": 0.08167},
    {"letter": "b", "frequency": 0.01492},
    {"letter": "c", "frequency": 0.02782},
    {"letter": "d", "frequency": 0.04253},
    {"letter": "e", "frequency": 0.12702},
    {"letter": "f", "frequency": 0.0228},
    {"letter": "g", "frequency": 0.02015},
    {"letter": "h", "frequency": 0.06094},
    {"letter": "i", "frequency": 0.06966},
    {"letter": "j", "frequency": 0.00153},
    {"letter": "k", "frequency": 0.00772},
    {"letter": "l", "frequency": 0.04025},
    {"letter": "m", "frequency": 0.02406},
    {"letter": "n", "frequency": 0.06749},
    {"letter": "o", "frequency": 0.07507},
    {"letter": "p", "frequency": 0.01929},
    {"letter": "q", "frequency": 0.00095},
    {"letter": "r", "frequency": 0.05987},
    {"letter": "s", "frequency": 0.06327},
    {"letter": "t", "frequency": 0.09056},
    {"letter": "u", "frequency": 0.02758},
    {"letter": "v", "frequency": 0.00978},
    {"letter": "w", "frequency": 0.0236},
    {"letter": "x", "frequency": 0.0015},
    {"letter": "y", "frequency": 0.01974},
    {"letter": "z", "frequency": 0.00074}
]

def find_key_shift(text):
    alphabet_frequencies = eng_frequencies
    text_frequencies = encode.get_text_frequencies(text, eng_frequencies)
    shifts = {}
    for i in range(len(alphabet_frequencies)):
        absolute_val_array = np.abs(np.array(list(text_frequencies.values())) - alphabet_frequencies[i]['frequency'])
        smallest_difference_index = absolute_val_array.argmin()
        shifts[smallest_difference_index - i] = shifts.get(smallest_difference_index - i, 0) + 1
    max_num_shifts = max(shifts, key=lambda x: shifts[x])
    return max_num_shifts if max_num_shifts >= 0 else len(eng_frequencies) + max_num_shifts


def hack_vigenere(text):
    key_len = encode.casisci("".join(text))
    key = []
    for i in range(key_len):
        shift = find_key_shift(text[i::key_len])
        key.append(chr(ord('a') + shift))
    return "".join(key)


def keys_equality(key1, key2):
    arr1 = [char for char in key1]
    arr2 = [char for char in key2]
    counter = 0
    for i in range(min(len(arr1), len(arr2))):
        if arr1[i] == arr2[i]:
            counter += 1
    return counter / max(len(arr1), len(arr2))


def perform_tests(num_tests = 100):
    demo_keys = ['zx', 'ryh', 'gqpl', 'hjsiz', 'zqwerm', 'mpqzjga', 'qrtogdan', 'zxcvbnmlk', 'omqfvijktp',
                 'pkdajpiltwm']
    casisci_statistics = [[0 for i in range(num_tests)] for i in range(num_tests)]
    dz = [0 for i in range(num_tests * num_tests)]
    for text_iter in range(num_tests):
        input_characters = file_funcsc.read_file('texts/big' + str(text_iter + 1) + '.txt')
        for cur_inter in range(num_tests):
            cur_key = demo_keys[cur_inter]
            for text_len in range(num_tests):
                rand_num = random.randint(0, len(input_characters) - (text_len + 1) * 1000)
                test_text = input_characters[rand_num: rand_num + (text_len + 1) * 1000]
                encrypted = decode.vigenere(test_text, cur_key)
                hacked_key = hack_vigenere(encrypted)
                print('text ', text_iter + 1, ', \nkey ', len(cur_key), ', \nlen text ', len(test_text))
                print('hacked key = ', hacked_key)
                print('equality percent = ', keys_equality(cur_key, hacked_key))
                dz[text_len * num_tests + len(cur_key) - len(demo_keys[0])] += ((hacked_key == cur_key) / num_tests)
                casisci_statistics[len(cur_key) - len(demo_keys[0])][text_len] += len(hacked_key) == len(cur_key)
    # print('casisci tests statistics')
    # for row in casisci_statistics:
    #     print(row)
    return dz


if __name__ == '__main__':
    # dz = perform_tests(num_tests)
    # file_funcsc.write_probabilities('texts/probabilities.txt', dz)
    dz = file_funcsc.read_probabilities('texts/probabilities.txt')
    dx, xpos, ypos, zpos = [], [], [], []
    dy = np.ones(100)
    for i in range(10):
        for j in range(10):
            xpos.append((i + 1) * 1000)
            ypos.append(j + 2)
            zpos.append(0)
            dx.append(1000)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('text len')
    ax.set_ylabel('key len')
    ax.set_zlabel('probability')
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
    plt.margins(0)
    plt.show()