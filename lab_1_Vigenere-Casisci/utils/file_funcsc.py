def read_file(path):
    file = open(path, 'r+', encoding='utf-8')
    characters = [elem for elem in file.read()]
    file.close()
    return characters


def write_probabilities(path, content):
    file = open(path, "w", encoding='utf-8')
    for elem in content:
        file.write(str(elem))
        file.write('\n')
    file.close()


def read_probabilities(path):
    file = open(path, 'r+', encoding='utf-8')
    characters = [float(elem) for elem in file.readlines()]
    file.close()
    return characters


def str_to_bool(string):
    return string == 'True'
