from pickle import TRUE
import sys
sys.path.append("D:/image_labelling")
from yaml_parser.parser import Parser
import matplotlib.pyplot as plt 
import cv2
import glob
import shutil
import os
class PopulationSelection(Parser):
    def __init__(self):
        super().__init__()
        self.z_score={80:1.28, 85:1.44, 90:1.65, 95:1.96, 99:2.58}                        # confidence : z score

    def __calculatesample_size(self,population_size):
        z = self.z_score[self.confidence_level]
        p = 0.50
        e = self.margin_of_error
        print(p)
        print(z)
        numerator = (z**2)*p*(1-p)/(e**2)
        print(numerator)
        sample_size = numerator//(1+(numerator/population_size))

        return sample_size+1

    def takeinput(self,image):
        path = image
        image=cv2.imread(image)
        image=cv2.resize(image,(512,512))
        # cv2.imshow("input the correct label for the image curent label is",image)
        plt.imshow(image)
        plt.show()
        input_class = input().lower()
        if path.split("\\")[-2] == input_class:
            return True,input_class
        return False,input_class


    def determine(self,correct,image):
        if correct:
            dest_path=self.save_data_path
        else:
            dest_path = self.ref_data_path
        shutil.move(image,dest_path)
        

    def call(self):
        directory=glob.glob('D:/image_labelling/TobePrompted/tennis/*')
        print(directory)
        for classes in directory:

            images=glob.glob(classes + '/*')
            population_size = len(images)
            size_to_be_prompted = self.__calculatesample_size(len(images))
            i=0
            accuracy = 0
            while size_to_be_prompted > 0:
                path=images[i]
                correct , label = self.takeinput(path)
                i+=1
                if correct:
                    accuracy+=1
                self.determine(correct,path)


if __name__=='__main__':
    p=PopulationSelection()
    p.call()
    # shutil.move('D:/image_labelling/TobePrompted/tennis\\serve\\71.png','D:/image_labelling/buckets/tennis/backhand')
    # cv2.imshow('verify the image is of',cv2.imread('D:/image_labelling/buckets/tennis/backhand/1.png'))
    # cv2.waitKey(0)
    # p.takeinput('D:/image_labelling/buckets/tennis/backhand/1.png')
    # print(p.calculatesample_size(10))

        