from configparser import ConfigParser
from os import getcwd


print(getcwd())

config = ConfigParser()
config.read('config.txt')
