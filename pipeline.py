from glob import glob
import sys
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
    for i in sorted(glob(src_data_path)):
        # _plot_graph(cv2.imread(i))
        
        alg = Algorithms()
        class_name = alg.selection_algorithms_available[selection_algorithm.lower()]['class_name']
        module_name = "selection_algorithms."+alg.selection_algorithms_available[selection_algorithm.lower()]["file_name"]            
        selection_class = getattr(importlib.import_module(module_name), class_name)
        
        res_obj = selection_class()
        individual_class_avg_scores = dict()
        for ref_class_folder in sorted(glob(ref_data_path)):
            individual_class_avg_scores[ref_class_folder.split("\\")[-1]] = 0
            for ref_img in sorted(glob(ref_class_folder+'/*')):
                individual_class_avg_scores[ref_class_folder.split("\\")[-1]] += res_obj.get_res(plugins, i, ref_img)
                print(res_obj.get_res(plugins, i, ref_img))
        
        # print(selection_class)