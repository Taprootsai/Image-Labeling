import sys
sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms

class Average(Algorithms):
    def __init__(self):
        super().__init__()
    
    def get_res(self, plugins):
        sum = 0
        plugin_scores = super().generate_scores(plugins)
        #calculate average of plugin scores
        for plugin in plugin_scores.keys():
            sum += plugin_scores[plugin]
        return sum/len(plugin_scores.keys())