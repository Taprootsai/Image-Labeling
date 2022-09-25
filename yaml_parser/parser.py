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
        self.plugins = self.configuration['plugin']
        self.selection_algorithms = self.configuration['selection_algorithm']
        self.src_data_mode = self.configuration['src_data_mode']
        self.src_data_path = self.configuration['src_data_path']
        self.ref_data_path = self.configuration['ref_data_path']
        self.save_data_path = self.configuration['save_data_path']
        self.src_data_url = self.configuration['src_data_url']
        self.confidence_level = self.configuration['confidence_level']
        self.margin_of_error = self.configuration['margin_of_error']

    def get_config(self):
        # print(self.configuration)
        # print(self.selection_algorithms)
        return self.configuration

class compute(Parser):
    def __init__(self):
        super().__init__()
        # self.configuration = 
    def print(self):
        print(self.selection_algorithms)
    