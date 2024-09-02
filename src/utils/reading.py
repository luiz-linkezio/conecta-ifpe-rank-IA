def read_txt_latin1(path):
    with open(path, 'r', encoding='latin-1') as file:
        txt = file.read().splitlines()

    return txt