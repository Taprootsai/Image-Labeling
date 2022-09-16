import inspect
import cv2
import sys
import abc

sys.path.append('E:/Open source/Image-Labeling')
from plugins.plugin import PLUGIN

# pe = PersonExtraction("../downloaded_models/yolo.h5")
# racket,person,racket_mid,person_mid = pe.extract("../ref_images/tennis/backhand/1.png",0.75)
# cv2.imshow("person",person)
# cv2.waitKey()
# cv2.imshow("racket",racket)
# cv2.waitKey()

class TEST(PLUGIN):
    def __init__(self):
        print("hi")
        
    def compare_images(self):
        #must implement this method in sub classes
        pass

if __name__ == "__main__":
    t = TEST()
    t.compare_images("","")
