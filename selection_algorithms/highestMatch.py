import sys
sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms

class HighestMatch(Algorithms):
    def __init__(self):
        super().__init__()
    
    def get_res(self, plugins, img_path, ref_img_path):
        plugin_scores = super().generate_scores(plugins, img_path, ref_img_path)
        highest_match = 0
        highest_match_plugin = ""
        return plugin_scores
 
    