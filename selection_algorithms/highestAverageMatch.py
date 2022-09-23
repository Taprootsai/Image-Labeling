import sys
sys.path.append('E:/Open source/Image-Labeling')
import glob
from selection_algorithms.algorithms import Algorithms

'''
This algorithm is used to classify the image to particular class using similarity scores of different plugins. one such algorithm is Highest Average Match,
It is obtained by averaging over similarity score for different plugins for each class. From resulting scores the class with highest score is considered to be label fo that image.
'''	


class HighestAverageMatch(Algorithms):
    def __init__(self):
        super().__init__()
    
    def get_res(self, plugins, img_path, ref_img_path):
        
        available_classes = list()
        for i in sorted(glob.glob(ref_img_path+'/*')):
            available_classes.append(i.split("/")[-1])
        
        all_plugin_scores = super().generate_scores(plugins, img_path, ref_img_path)
        print(all_plugin_scores)
        avg = dict()#avg of all plugins for individual classes
        
        for classes in available_classes:
            sum_ = 0    
            for individual_plugin_score in all_plugin_scores.keys():
                # print(all_plugin_scores[individual_plugin_score])
                sum_ += all_plugin_scores[individual_plugin_score][classes]
            avg[classes] = sum_/len(plugins)
        print(avg)
        highest_score = 0
        highest_class = ""
        for i in avg.keys():
            if avg[i] > highest_score:
                highest_score = avg[i]
                highest_class = i
        return highest_class.split("\\")[-1], highest_score