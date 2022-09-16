import glob
import sys
import os
import cv2
import matplotlib.pyplot as plt
import importlib

from selection_algorithms.algorithms import Algorithms

sys.path.append('E:/Open source/Image-Labeling')

from yaml_parser.parser import Parser

pr = Parser()
configuration = pr.get_config()

plugins = configuration['plugin']
selection_algorithm = configuration['selection_algorithm']
src_data_mode = configuration['src_data_mode']
src_data_path = configuration['src_data_path']
ref_data_path = configuration['ref_data_path']
save_data_path = configuration['save_data_path']

def _plot_graph(image):
    plt.imshow(image, cmap = plt.cm.gray)
    plt.axis("off")
    plt.show()

if src_data_mode=="local":
    alg = Algorithms()
    class_name = alg.selection_algorithms_available[selection_algorithm.lower()]['class_name']
    module_name = "selection_algorithms."+alg.selection_algorithms_available[selection_algorithm.lower()]["file_name"]            
    selection_class = getattr(importlib.import_module(module_name), class_name)
    selection_obj = selection_class()
    
    for i in sorted(glob.glob(src_data_path+'/*')):
        # _plot_graph(cv2.imread(i))
           
        #TODO: Add support for bucketizing folder of test data(multiple test images maybe video)
        bucket,score = selection_obj.get_res(plugins, i, ref_data_path)
        
        if not os.path.exists(save_data_path+"/"+bucket):
            os.makedirs(save_data_path+"/"+bucket)
        print("\n\n"+i.split("\\")[-1])
        print("\n\n"+save_data_path)
        cv2.imwrite(save_data_path+"/"+bucket+"/"+i.split("\\")[-1], cv2.imread(i))
        
        # print(selection_class)