import sys

from plugins.ssim import SSIM
from plugins.orb import ORB

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
        self.classes = dict()
        for i in self.get_plugins_available():
            print(i)
            self.classes[i] = getattr(sys.modules[__name__], i.upper())
            
    def get_plugins_available(self):
        return self.plugins_available
    
    def get_selection_algorithms_available(self):
        return self.selection_algorithms_available
    
    def get_plugins_scores(self):
        return self.plugin_scores        
    
    def _get_plugin_obj(self, class_name):
        return self.classes[class_name]()
          
    def generate_scores(self, selection_algorithm, plugins):
        #There can be many plugins but only one result selection algorithm
        if selection_algorithm in self.selection_algorithms_available:
            print("selection algorithm available")
            if set(plugins).issubset(set(self.plugins_available)):
                print("\n\nplugin available.....Generating similarity scores\n\n")
                for i in set(plugins):
                    j = self._get_plugin_obj(i)
                    scores = j.compare_images('ref_images/tennis/backhand/1.png','ref_images/tennis/serve/1.png')
                    self.plugin_scores[i] = scores
            else:
                print("Plugin not available")
        else:
            print("Selection algorithm not available")