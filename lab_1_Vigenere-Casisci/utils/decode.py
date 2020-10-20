def get_basis(is_caps):
    return 'A' if is_caps else 'a'


def is_letter(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z'


def is_capital(letter):
    return 'A' <= letter <= 'Z'


def normalize_size(letter, is_caps):
    basis = get_basis(is_caps)
    return chr(((ord(letter) - ord(basis)) % 26) + ord(basis))


def vigenere_shift(letter, is_caps):
    return ord(letter) - ord(get_basis(is_caps))


def vigenere(array, key, enc=True):
    key_length = len(key)
    key_list = list(map(lambda x: {'chr': x, 'is_caps': is_capital(x)}, key))
    answer = []
    for i in range(len(array)):
        letter = array[i]
        if is_letter(letter):
            is_caps = is_capital(letter)
            shift = vigenere_shift(key_list[i % key_length]['chr'], key_list[i % key_length]['is_caps'])
            answer.append(normalize_size(chr(ord(letter) + (shift if enc else -shift)), is_caps))
        else:
            answer.append(letter)
    return answer


def cesar(array, shift, enc=True):
    answer = []
    for i in range(len(array)):
        if is_letter(array[i]):
            is_caps = is_capital(array[i])
            answer.append(normalize_size(chr(ord(array[i]) + (shift if enc else -shift)), is_caps))
        else:
            answer.append(array[i])
    return answer
