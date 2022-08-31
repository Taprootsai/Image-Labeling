from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
from cProfile import label
import os
import sys
from Helpers.person_extraction import PersonExtraction

class Ssim:
    def __init__(self,model_path):
        self.pe = PersonExtraction(model_path=model_path)

    def _extract_person(self,img_path):
        racket,person,racket_mid,person_mid = self.pe.extract(img_path,0.75)
        # cv2.imshow("person",person)
        # cv2.waitKey()
        return person
    
    def compare_images(self, imageA, imageB):
        # cv2_imshow(imageA)
        # cv2_imshow(imageB)
        imageA = self._extract_person(imageA)
        imageB = self._extract_person(imageB)
        
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        imageA = cv2.resize(imageA, imageB.shape[::-1])
        # print(imageA.shape)
        # print(imageB.shape)
        s = ssim(imageA, imageB,fullbool=True)
        fig = plt.figure("comaprision")
        plt.title(f"ssim score: {s}")
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(imageA, cmap = plt.cm.gray)
        plt.axis("off")

        ax = fig.add_subplot(1, 2, 2)
        plt.imshow(imageB, cmap = plt.cm.gray)
        plt.axis("off")
    
        plt.show()
        return s


