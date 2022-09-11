import yaml
import sys
import importlib.util
# spec  = importlib.util.spec_from_file_location('orb','D:/image_labelling/plugins/orb.py')
# orb = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(orb)
# print(orb.ORB())
from yaml.loader import SafeLoader
sys.path.append('/image_labelling/plugins')
from orb import ORB
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