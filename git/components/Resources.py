import copy
from os import listdir
from os.path import join, dirname, realpath
import configparser
from flask import json


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

    @staticmethod
    def getConfigs():
        dir = join(dirname(realpath(__file__)), 'resources', 'conf')
        configs_files = listdir(dir)
        configs = {}

        for file in configs_files:
            if file.endswith('.ini'):
                parser = configparser.RawConfigParser()
                parser.read(join(dir, file))
                configs[file] = parser._sections

        return configs

    @staticmethod
    def Settings(opt):
        with open(join('components', 'resources', 'settings.json')) as data_file:
            data = json.load(data_file)

        return data[opt]