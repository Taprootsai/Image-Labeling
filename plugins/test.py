import cv2
import sys
sys.path.append('E:/Open source/Image-Labeling')

from plugins.Helpers.person_extraction import PersonExtraction
from ssim import SSIM

# pe = PersonExtraction("../downloaded_models/yolo.h5")
# racket,person,racket_mid,person_mid = pe.extract("../ref_images/tennis/backhand/1.png",0.75)
# cv2.imshow("person",person)
# cv2.waitKey()
# cv2.imshow("racket",racket)
# cv2.waitKey()

s1 = SSIM(model_path="downloaded_models/yolo.h5")
s1.compare_images("ref_images/tennis/backhand/1.png","ref_images/tennis/serve/1.png")
