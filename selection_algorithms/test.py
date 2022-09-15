import sys

sys.path.append('E:/Open source/Image-Labeling')

from selection_algorithms.algorithms import Algorithms
from selection_algorithms.highestMatch import HighestMatch
from selection_algorithms.average import Average

hm = Average()
print(hm.get_res(['ssim','orb']))

