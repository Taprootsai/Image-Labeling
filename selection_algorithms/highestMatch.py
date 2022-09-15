import sys
sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms

class HighestMatch(Algorithms):
    def __init__(self):
        super().__init__()
    
    def get_res(self, plugins):
        plugin_scores = super().generate_scores(plugins)
        highest_match = 0
        highest_match_plugin = ""
        for plugin in plugin_scores.keys():
            if plugin_scores[plugin] > highest_match:
                highest_match_score = plugin_scores[plugin]
                highest_match_plugin = plugin
        return highest_match_score, highest_match_plugin
 
    