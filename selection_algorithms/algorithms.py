import sys
import importlib
from plugins.ssim import SSIM
from plugins.orb import ORB

sys.path.append('E:/Open source/Image-Labeling')

import json

class Algorithms:
    def __init__(self):
        #get available plugins
        metadata = json.load(open('metadata.json'))
        self.plugins_available = metadata.get('plugins')
        self.selection_algorithms_available = metadata.get('selection_algorithms')

        #To store plugin results
        self.plugin_scores = dict()
        for i in self.plugins_available:
            self.plugin_scores[i] = 1
        
        #Mapping between plugin names (str) to respective class  
        self.plugin_classes = dict()
        for i in self.plugins_available:
            self.plugin_classes[i] = getattr(sys.modules[__name__], i.upper())
        print(self.plugin_classes)
        
        self.selection_classes = dict()
        for i in self.selection_algorithms_available:
            class_name = self.selection_algorithms_available[i]["class_name"]
            module_name = "selection_algorithms."+self.selection_algorithms_available[i]["file_name"]            
            self.selection_classes[i] = getattr(importlib.import_module(module_name), class_name)
        print(self.selection_classes)
        
    def get_plugins_available(self):
        return self.plugins_available
    
    def get_selection_algorithms_available(self):
        return self.selection_algorithms_available
    
    def get_plugins_scores(self):
        return self.plugin_scores        
    
    #Creates plugin obj for given plugin name
    def _get_plugin_obj(self, class_name):
        return self.plugin_classes[class_name]()
    
    #Creates selection algorithm obj for given selection algorithm name
    def _get_selection_algorithm_obj(self, class_name):
        return self.selection_classes[class_name]()
    
    def generate_scores(self, plugins):
        #There can be many plugins but only one result selection algorithm
        if set(plugins).issubset(set(self.plugins_available)):
            print("\n\nplugin available.....Generating similarity scores\n\n")
            for i in set(plugins):
                j = self._get_plugin_obj(i)
                scores = j.compare_images('ref_images/tennis/backhand/1.png','ref_images/tennis/serve/1.png')
                self.plugin_scores[i] = scores
        else:
            print("Plugin not available")
        return self.plugin_scores
    
    def get_res(self, plugins):
        #implement selection algorithm in subclasses
        pass