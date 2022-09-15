import sys
sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms

class Average(Algorithms):
    def __init__(self):
        super().__init__()
    
    def get_res(self, plugins, img_path, ref_img_path):
        plugin_scores = super().generate_scores(plugins, img_path, ref_img_path)
        _sum = 0
        #calculate average of plugin scores
        for plugin in plugin_scores.keys():
            _sum += plugin_scores[plugin]
        return _sum/len(plugin_scores.keys())