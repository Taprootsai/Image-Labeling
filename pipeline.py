import glob
import sys
import os
import cv2
import matplotlib.pyplot as plt
import importlib
import json

from selection_algorithms.algorithms import Algorithms

sys.path.append('E:/Open source/Image-Labeling')

from yaml_parser.parser import Parser

class Pipeline:
    def __init__(self):
        pr = Parser()
        configuration = pr.get_config()

        self.plugins = configuration['plugin']
        self.selection_algorithm = configuration['selection_algorithm']
        self.src_data_mode = configuration['src_data_mode']
        self.src_data_path = configuration['src_data_path']
        self.ref_data_path = configuration['ref_data_path']
        self.save_data_path = configuration['save_data_path']
        
        metadata = json.load(open('.metadata.json'))
        self.selection_algorithms_available = metadata.get('selection_algorithms')
        
        self.selection_classes = dict()
        for i in self.selection_algorithms_available:
            class_name = self.selection_algorithms_available[i]["class_name"]
            module_name = "selection_algorithms."+self.selection_algorithms_available[i]["file_name"]            
            self.selection_classes[i] = getattr(importlib.import_module(module_name), class_name)

    def _plot_graph(self,image):
        plt.imshow(image, cmap = plt.cm.gray)
        plt.axis("off")
        plt.show()

    def start_bucketizing(self,):
        if self.src_data_mode=="local":
            # alg = Algorithms()
            class_name = self.selection_algorithms_available[self.selection_algorithm.lower()]['class_name']
            module_name = "selection_algorithms."+self.selection_algorithms_available[self.selection_algorithm.lower()]["file_name"]            
            selection_class = getattr(importlib.import_module(module_name), class_name)
            selection_obj = selection_class()
            
            for i in sorted(glob.glob(self.src_data_path+'/*')):
                # _plot_graph(cv2.imread(i))
                
                bucket,score = selection_obj.get_res(self.plugins, i, self.ref_data_path)
                
                if not os.path.exists(self.save_data_path+"/"+bucket):
                    os.makedirs(self.save_data_path+"/"+bucket)
                if not os.path.exists(self.save_data_path+"/"+bucket+"/"+i.split("\\")[-1]):
                    cv2.imwrite(self.save_data_path+"/"+bucket+"/"+i.split("\\")[-1], cv2.imread(i))
                
                # print(selection_class)