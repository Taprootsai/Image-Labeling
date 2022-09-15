from ast import parse
from email import parser
import sys

sys.path.append('E:/Open source/Image-Labeling')

from yaml_parser.parser import Parser

parser = Parser()
config = parser.get_config()  	
print(config)
    