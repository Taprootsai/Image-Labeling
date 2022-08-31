import os
import sys
from turtle import left
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import glob
import numpy as np
import pandas as pd
from requests import head
import pickle
from imageai.Detection import ObjectDetection   

raw_img_height = 1080
raw_img_width = 1920

class PersonExtraction:
    #constructor of the class
    def __init__(self, model_path):
        self.detector = ObjectDetection() 
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath(model_path)

        self.custom = self.detector.CustomObjects(person=True,tennis_racket=True)
        self.detector.loadModel()
        self.person_detected = False
        self.racket_detected = False
    
    def _read_img(self,raw_img):    
        raw_img = cv2.imread(raw_img)                                                                            
        raw_img = cv2.resize(raw_img, (raw_img_width, raw_img_height))[540:1080,:]                                  ###image is directly provider remove the imagepath
        return raw_img
    
    def _detect(self,raw_img, min_percent):
        detections = self.detector.detectCustomObjectsFromImage(custom_objects=self.custom, input_type="array",input_image=raw_img, output_image_path="temp.png", minimum_percentage_probability=min_percent)
        try: 
            os.remove("temp.png")
        except: 
            pass
        return detections
    
    def _extract_entities(self, detections):
        person_detections = []
        racket_detections = []
        for item in detections:
            if item['name']=="person":
                person_detections.append(item)
            elif item['name']=="tennis racket":
                racket_detections.append(item)
            
        person_detections = sorted(person_detections, key = lambda item: item['percentage_probability'], reverse=True)
        racket_detections = sorted(racket_detections, key = lambda item: item['percentage_probability'], reverse=True)
        return person_detections, racket_detections
    
    def _get_box_points(self, entity_detection):
        left = entity_detection[0]['box_points'][0]
        top = entity_detection[0]['box_points'][1]
        right = entity_detection[0]['box_points'][2]
        bottom = entity_detection[0]['box_points'][3]
        return left,right,bottom,top

    def _extract_mid_point(self,left,right,bottom,top):
        return ((int)((right+left)/2), (int)((540-top+540-bottom)/2))
    
    def _extract_individual_entity(self,raw_img,left,right,bottom,top):
        # raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        if top-100>0:
            top = top-100
        if left-100>0:
            left = left-100
        if right+100<raw_img_width:
            right = right+100
        extracted_entity = raw_img[top:bottom,left:right]
        mid_point = self._extract_mid_point(left,right,bottom,top)
        return extracted_entity, mid_point
    
    def _process(self,raw_img,racket_detections,person_detections):
        racket = None
        person = None
        mid_point_racket = None
        mid_point_person = None
        if len(racket_detections) != 0:
            left,right,bottom,top = self._get_box_points(racket_detections)
            racket,mid_point_racket = self._extract_individual_entity(raw_img,left,right,bottom,top)
            self.racket_detected=True

        if len(person_detections) != 0:
            left,right,bottom,top = self._get_box_points(person_detections)
            person,mid_point_person = self._extract_individual_entity(raw_img,left,right,bottom,top)
            self.person_detected=True

        return racket,person,mid_point_racket,mid_point_person
        
    
    def extract(self,raw_img_path, min_percent):                                              
        raw_img = self._read_img(raw_img_path)
        detections = self._detect(raw_img, min_percent)
        person_detections, racket_detections = self._extract_entities(detections)
        return self._process(raw_img,racket_detections,person_detections)