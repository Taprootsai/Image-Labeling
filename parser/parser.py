import yaml
import sys

from yaml.loader import SafeLoader
sys.path.append('/image_labelling/')

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
        return self.configuration

    


if __name__=='__main__':
    pr=Parser()
    # com=compute()
    # com.print()
    print(pr.get_config())