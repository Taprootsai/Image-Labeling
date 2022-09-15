import yaml
import sys

# sys.path.append('E:/Open source/Image-Labeling')


class Parser:
    def __init__(self):
        self.file_name='config.yaml'

        with open('config.yaml') as f:

            self.configuration = yaml.full_load(f)
        self.__initiate()
    def __initiate(self):
        self.metrics = self.configuration['plugin']
        self.algos = self.configuration['selection_algorithm']

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
    