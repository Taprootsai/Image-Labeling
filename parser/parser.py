import yaml
import sys
from yaml.loader import SafeLoader
sys.path.append('E:/Open source/Image-Labeling')
from plugins.orb import ORB
class Parser:
    def __init__(self):
        self.file_name='config.yaml'

        with open('config.yaml') as f:

            self.configuration = yaml.full_load(f)
        self.__initiate()
    def __initiate(self):
        self.metrics = self.configuration['algorithm']
        self.algos = self.configuration['matrix']

    def get_config(self):
        # print(self.configuration)
        # print(self.algos)
        return self.configuration

class compute(Parser):
    def __init__(self):
        super().__init__()
        # self.configuration = 
    def print(self):
        print(self.algos)
    


if __name__=='__main__':
    pr=Parser()
    com=compute()
    com.print()
    pr.get_config()