import sys

sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms
from selection_algorithms.highestAverageMatch import HighestMatch
from selection_algorithms.average import Average

hm = HighestMatch()
print(hm.get_res(['ssim','orb'], 'ref_images/tennis/forehand/1.png', 'ref_images/tennis'))

