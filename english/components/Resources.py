from os.path import join


class Resources:
    def __init__(self):
        pass

    @staticmethod
    def read(file):
        with open(file, 'r') as f:
            read_data = f.read()
        return read_data

    @staticmethod
    def readStyleSheet(file):
        return Resources.read(join('assets', 'styles', file))