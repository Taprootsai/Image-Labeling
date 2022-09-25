import sys
import importlib
import glob
import abc
from plugins.ssim import SSIM
from plugins.orb import ORB

sys.path.append('E:/Open source/Image-Labeling')

import json

class Algorithms(metaclass=abc.ABCMeta):	
    def __init__(self):
        #get available plugins
        metadata = json.load(open('.metadata.json'))
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
        # print(self.plugin_classes)
        
        self.selection_classes = dict()
        for i in self.selection_algorithms_available:
            class_name = self.selection_algorithms_available[i]["class_name"]
            module_name = "selection_algorithms."+self.selection_algorithms_available[i]["file_name"]            
            self.selection_classes[i] = getattr(importlib.import_module(module_name), class_name)
        # print(self.selection_classes)
        
    def get_plugins_available(self):
        return self.plugins_available
    
    def get_selection_algorithms_available(self):
        return self.selection_algorithms_available
    
    def get_plugins_scores(self):
        return self.plugin_scores        
    
    #Creates plugin obj for given plugin name
    def __get_plugin_obj(self, class_name):
        return self.plugin_classes[class_name]()
    
    #Creates selection algorithm obj for given selection algorithm name
    # def __get_selection_algorithm_obj(self, class_name):
    #     return self.selection_classes[class_name]()
    
    def __get_individual_class_avg_score(self,plugin_obj, img_path, ref_img_path):
        individual_class_avg_score = dict()
        for individual_classes in sorted(glob.glob(ref_img_path+'/*')):
            sum_=0
            for images in sorted(glob.glob(individual_classes+'/*')):
                sum_ += plugin_obj.compare_images(img_path, images)
            individual_class_avg_score[individual_classes.split("/")[-1]] = sum_/len(glob.glob(individual_classes+'/*'))
        return individual_class_avg_score
    
    def generate_scores(self, plugins,img_path, ref_img_path):
        #There can be many plugins but only one result selection algorithm
        if set(plugins).issubset(set(self.plugins_available)):
            print("\n\nplugin available.....Generating similarity scores\n\n")
            for individual_plugin in set(plugins):
                plugin_obj = self.__get_plugin_obj(individual_plugin)
                scores = self.__get_individual_class_avg_score(plugin_obj, img_path, ref_img_path)
                self.plugin_scores[individual_plugin] = scores
        else:
            print("Plugin not available")
        return self.plugin_scores
    
    @abc.abstractclassmethod
    def get_res(self, plugins, img_path, ref_img_path):
        #implement selection algorithm in subclasses
        pass