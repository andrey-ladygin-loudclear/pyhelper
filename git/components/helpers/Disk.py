from os import listdir
from shutil import copyfile


class Disk:
    def __init__(self, commandObject):
        pass

    def copyPems(self, args):
        dir = '/home/andrey/pems/'
        pems = listdir(dir)
        dst = 'components/resources/pems/'

        for file in pems:
            if file.endswith('.pem'):
                print('copy: '+dst + file)
                copyfile(dir + file, dst + file)

    def copyConfFrom(self, args):
        pass

    def copyConfTo(self, args):
        pass