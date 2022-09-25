from genericpath import isfile
import glob
from itertools import count
import sys
import os
import cv2
import matplotlib.pyplot as plt
import importlib
import json
from selection_algorithms.algorithms import Algorithms
import urllib
sys.path.append('E:/Open source/Image-Labeling')

from yaml_parser.parser import Parser

class Pipeline:
    def __init__(self):
        pr = Parser()
        configuration = pr.get_config()

        self.plugins = configuration['plugin']
        self.selection_algorithm = configuration['selection_algorithm']
        self.src_data_mode = configuration['src_data_mode']
        self.src_data_path = configuration['src_data_path']
        self.ref_data_path = configuration['ref_data_path']
        self.save_data_path = configuration['save_data_path']
        self.src_data_url = configuration['src_data_url']
        
        metadata = json.load(open('.metadata.json'))
        self.selection_algorithms_available = metadata.get('selection_algorithms')
        
        self.selection_classes = dict()
        for i in self.selection_algorithms_available:
            class_name = self.selection_algorithms_available[i]["class_name"]
            module_name = "selection_algorithms."+self.selection_algorithms_available[i]["file_name"]            
            self.selection_classes[i] = getattr(importlib.import_module(module_name), class_name)

    def _plot_graph(self,image):
        plt.imshow(image, cmap = plt.cm.gray)
        plt.axis("off")
        plt.show()
    
    def _no_of_images_labeled(self):
        count = 0
        if os.path.exists(self.save_data_path):
            for i in os.listdir(self.save_data_path):
                count += len(os.listdir(self.save_data_path+"/"+i))        
        return count 
    
    def _calculate_avg_mean_each_img(self,path):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pixel_sum = 0
        no_of_pixels = img.shape[0]*img.shape[1]
        for k in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel_sum += img[k][j]
        return pixel_sum/no_of_pixels
    
    def _calculate_avg_mean(self):
        avg_mean_dict = dict()
        for i in os.listdir(self.ref_data_path):
            avg_mean_dict[str(i)] = 0
            class_sum =0 
            for images in os.listdir(self.ref_data_path+"/"+i):
                mean_of_curr_img = self._calculate_avg_mean_each_img(self.ref_data_path+"/"+i+"/"+images)
                class_sum += mean_of_curr_img
            avg_mean_dict[str(i)] = class_sum/len(os.listdir(self.ref_data_path+"/"+i))
        return avg_mean_dict
    
    def _choose_population_for_oracle(self,start,avg_mean_dict):
        for i in range(start-1,start+20):
            for labeled_data_domain in os.listdir(self.save_data_path):
                # print(self.save_data_path+"/"+labeled_data_domain+"/"+str(i)+".png")
                if os.path.isfile(self.save_data_path+"/"+labeled_data_domain+"/"+str(i)+".png"):
                    curr_img_path = self.save_data_path+"/"+labeled_data_domain+"/"+str(i)+".png"
                    curr_img_pixel_mean = self._calculate_avg_mean_each_img(curr_img_path)
                    difference = abs(curr_img_pixel_mean - avg_mean_dict[labeled_data_domain])
                    if difference >= 5:
                        if not os.path.exists("to_oracle"+"/"+self.save_data_path.split("/")[-1]):
                            os.makedirs("to_oracle"+"/"+self.save_data_path.split("/")[-1])
                        if not os.path.exists("to_oracle"+"/"+self.save_data_path.split("/")[-1]+"/"+str(i)+".png"):
                            cv2.imwrite("to_oracle"+"/"+self.save_data_path.split("/")[-1]+"/"+str(i)+".png", cv2.imread(curr_img_path))
                    print(f"img : {curr_img_pixel_mean}")
                    print(f"ref : {avg_mean_dict[labeled_data_domain]}")

    def start_bucketizing(self):
        if self.src_data_mode!="local":
            src_img_save_save_path = "test_data/{}.png".format(len(os.listdir("test_data"))+1)
            img = urllib.request.urlretrieve(self.src_data_url, src_img_save_save_path)
            new_img = cv2.cvtColor(cv2.imread(img[0]), cv2.COLOR_BGR2GRAY)
            cv2.imwrite(src_img_save_save_path, new_img)
                    
        # Creates object of selection algorithm specified in config
        class_name = self.selection_algorithms_available[self.selection_algorithm.lower()]['class_name']
        module_name = "selection_algorithms."+self.selection_algorithms_available[self.selection_algorithm.lower()]["file_name"]            
        selection_class = getattr(importlib.import_module(module_name), class_name)
        selection_obj = selection_class()
        
        start = self._no_of_images_labeled()
        image_name=start
        no_of_images_labeled = start
        avg_mean_dict = self._calculate_avg_mean()

        for i in sorted(glob.glob(self.src_data_path+'/*')):
            # _plot_graph(cv2.imread(i))
            
            if(no_of_images_labeled%20==0 and no_of_images_labeled!=0):
                self._choose_population_for_oracle(start,avg_mean_dict)
            
            
            bucket,score = selection_obj.get_res(self.plugins, i, self.ref_data_path)
            
            if not os.path.exists(self.save_data_path+"/"+bucket):
                os.makedirs(self.save_data_path+"/"+bucket)
            if not os.path.exists(self.save_data_path+"/"+bucket+"/"+str(image_name)+".png"):
                cv2.imwrite(self.save_data_path+"/"+bucket+"/"+str(image_name)+".png", cv2.imread(i))
            image_name+=1
            no_of_images_labeled += 1
            start+=1
