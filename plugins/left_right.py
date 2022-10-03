import cv2
from plugins.orb import ORB
import glob
from plugins.Helpers.person_extraction import PersonExtraction
from plugins.Helpers.body_points import Bodypoints
from plugins.plugin import PLUGIN
import os
import pandas as pd
import re


class LEFT_RIGHT(PLUGIN):
  
  def __init__(self):
    self.results = pd.DataFrame(columns = ['frame_path', 'angles', 'classified_as'])
    self.bp = Bodypoints()
  
  def _classify_frame(self,imageA, dominant):
    
    angles = self.bp.process(imageA, '', 1, 1)  
    # print(f"angles={angles}")
    triangle_angles = self.bp.traingle_angle(imageA, '', 1, 1)  
    # print(f"triangle angles={triangle_angles}")
    
    res_class=""	
    if triangle_angles is None:
      print('Unable to detect points')
      return  

    if (triangle_angles[3]>175 and triangle_angles[3]<185): 
      self.results.loc[len(self.results)] = [imageA,angles,0]
      res_class = 'serve'
    else:
      if triangle_angles[4]==True:
        res_class = 'forehand'
        self.results.loc[len(self.results)] = [imageA,angles,1]
      else:
        res_class = 'backhand'
        self.results.loc[len(self.results)] = [imageA,angles,2]
      
    return res_class
  
  def compare_images(self,imageA,imageB):      
      # print(f'\n{imageA}')
      res_class_A = self._classify_frame(imageA,dominant=1)
      res_class_B = imageB.split('\\')[1]
      if res_class_A==res_class_B:
        return 1
      else:
        return 0