import sys
sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms
from selection_algorithms.highestMatch import HighestMatch

alg = Algorithms()
alg.generate_scores('majority',['ssim','orb'])
print(alg.get_plugins_scores())

