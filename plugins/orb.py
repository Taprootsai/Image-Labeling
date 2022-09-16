import sys

from plugins.plugin import PLUGIN
sys.path.append('E:/Open source/Image-Labeling')

from plugins.Helpers.person_extraction import PersonExtraction

import cv2
class ORB(PLUGIN):
    def __init__(self,threshold=0.75):
        # self.pe = PersonExtraction(model_path='downloaded_models/yolo.h5)
        self.threshold=threshold

    def _extract_person(self,img_path):
        # racket,person,racket_mid,person_mid = self.pe.extract(img_path,0.75)
        # # cv2.imshow("person",person)
        # # cv2.waitKey()
        # return person
        pass
    def __detection(self,imageA,imageB):
        detect = cv2.ORB_create()
        imageA = cv2.imread(imageA)
        imageB = cv2.imread(imageB)
        keypointsA, descriptorA = detect.detectAndCompute(imageA,None)
        keypointsB, descriptorB = detect.detectAndCompute(imageB,None)
        return (keypointsA,descriptorA,keypointsB,descriptorB)
    
    def __bf_mathcer(self, descA,descB):
        matcher=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
        no_of_matches=matcher.match(descA,descB)
        most_similar_regions=[i for i in no_of_matches if i.distance<50]
        return most_similar_regions,len(most_similar_regions)/len(no_of_matches)

    # def __display_output(self,pic1,kpt1,pic2,kpt2,best_match):
    #     output_image = cv2.drawMatches(pic1,kpt1,pic2,kpt2,best_match[:],None,flags=2)
    #     cv2.imshow(output_image)
    
    def compare_images(self, imageA, imageB):
        # cv2.imshow(imageA)
        # cv2.imshow(imageB)
        # imgA=cv2.imread(imageA)
        # imgB=cv2.imread(imageB)
    
        key_ptA,descA,key_ptB,descB=self.__detection(imageA,imageB)
        no_of_matches ,orb_score = self.__bf_mathcer(descA,descB)

        # self.__display_output(imageA,key_ptA,imageB,key_ptB,no_of_matches)

        return orb_score 

