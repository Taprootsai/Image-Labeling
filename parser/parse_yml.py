import yaml
from yaml.loader import SafeLoader

class Parser:
    def __init__(self):
        self.file_name='config.yaml'
        with open('config.yaml') as f:
            self.configuration = yaml.full_load(f)
    def get_config(self):
        print(self.configuration)
        return self.configuration


if __name__=='__main__':
    pr=Parser()
    pr.get_config()