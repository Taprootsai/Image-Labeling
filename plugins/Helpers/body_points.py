from plugins.Helpers.person_extraction import PersonExtraction
import numpy as np
import cv2
import matplotlib.pyplot as plt
import mediapipe as mp

class Bodypoints():

 def __init__(self,imageai_model_path="downloaded_models/yolo.h5") -> None:
   self.mp_pose = mp.solutions.pose
   self.pose_image = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
   #self.imgpath=rawpath   #[-1, 202.95865065889782, 134.60092979280236, 168.82674401141398, 234.31668391011084, 168.82674401141398, -1, 111.15530739650367, 1, 'serve']
   self.mp_drawing = mp.solutions.drawing_utils
   self.personExtractor = PersonExtraction(imageai_model_path)
   self.isperson_extracted=False

 def detect_pose(self,img,pose,draw,display):
   try:
     img_r=cv2.cvtColor(img.copy(),cv2.COLOR_BGR2RGB)
   except:
     pass
   r=pose.process(img_r)
   #print(r.pose_landmarks)
   if r is None:
       print("0")

   if r.pose_landmarks and draw:    
     self.mp_drawing.draw_landmarks(image=img, landmark_list=r.pose_landmarks,
                                   connections=self.mp_pose.POSE_CONNECTIONS,
                                   landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255,255,255),
                                                                               thickness=3, circle_radius=3),
                                   connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(49,125,237),
                                                                               thickness=2, circle_radius=2))
     if display:
         plt.figure(figsize=[22,22])
         plt.subplot(121);plt.imshow(img[:,:,::-1]);plt.title("Input Image");plt.axis('off');
         plt.subplot(122);plt.imshow(img[:,:,::-1]);plt.title("Pose detected Image");plt.axis('off');
     return r

 def get_landmarks(self,r):
   landmarks=r.pose_landmarks.landmark
   return landmarks

 def calculate_angle(self,a,b,c):
     a = np.array(a) # First
     b = np.array(b) # Mid
     c = np.array(c) # End
    
     radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
     angle = np.abs(radians*180.0/np.pi)
     
     #if angle >180.0:
     #   angle = 360-angle
     return angle

 def calculate_angle180(self,a,b,c):
     a = np.array(a) # First
     b = np.array(b) # Mid
     c = np.array(c) # End
     
     radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
     angle = np.abs(radians*180.0/np.pi)
     
     if angle >180.0:
         angle = 360-angle
         
     return angle

 def angle_lefthand(self,landmarks):
   shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
   elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
   wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
   angle = self.calculate_angle(shoulder, elbow, wrist)
   return angle

 def angle_righthand(self,landmarks):
   r_shoulder_ = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
   r_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
   r_wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
   r_angle=self.calculate_angle(r_shoulder_,r_elbow,r_wrist)
   del r_shoulder_
   del r_elbow
   del r_wrist
   return r_angle

 def angle_leftpose(self,landmarks):
   shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
   hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
   knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
   angle=self.calculate_angle(shoulder,hip,knee)
   del shoulder
   del hip
   del knee
   return angle

 def angle_rightpose(self,landmarks):
   shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
   hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
   knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
   angle=self.calculate_angle(shoulder,hip,knee)
   del shoulder
   del hip
   del knee
   return angle


 def angle_leftleg(self,landmarks):
   hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
   knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
   ankle = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
   angle=self.calculate_angle(hip,knee,ankle)
   del hip
   del knee
   del ankle
   return angle

 def angle_rightleg(self,landmarks):
   hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
   knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
   ankle = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
   angle=self.calculate_angle(hip,knee,ankle)
   del hip
   del knee
   del ankle
   return angle

 def angle_leftshouler_knee(self,landmarks):
   elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
   hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
   knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
   angle=self.calculate_angle(elbow,hip,knee)
   del elbow
   del hip
   del knee
   return angle

 def angle_rightshouler_knee(self,landmarks):
   elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
   knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
   hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
   angle=self.calculate_angle(elbow,hip,knee)
   del elbow
   del knee
   del hip
   return angle

 def angle_leftshouler(self,landmarks):
   elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
   hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
   shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
   angle=self.calculate_angle(elbow,shoulder,hip)
   del elbow
   del hip
   del shoulder
   return angle


 def angle_rightshouler(self,landmarks):
   elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
   hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
   shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
   angle=self.calculate_angle(elbow,shoulder,hip)
   del elbow
   del hip
   del shoulder
   return angle

 def ankle_dist(self,landmarks):
   lankle= [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
   rankle= [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

   sum_sq=np.sum(np.square(np.array(lankle)-np.array(rankle)))
   del lankle
   del rankle
   return np.sqrt(sum_sq)

# returns the angles calculated based on extracted image  dominate= 1 for right hand and name userage is used to generate the data 

# '''
# lh=left hand  angle at elbow
# rh=right hand angle at elbow
# lk= left hand shoulder with right knee
# rk=right  hand sholder with left knee
# rs=right shoulder
# ls=left shoulder
# lp=left pose  (angle with respect to right hip)
# rp=right pose 
# ll=left leg 
# rl=right leg
# userage flag to collect the data
# name indicates shot name for collecting data
# '''
 def process(self,rawimage,name,dominate,useage):                                          
     lh=-1
     rh=-1
     ls=-1
     rs=-1
     rk=-1
     lk=-1
     #temp = self.imgpath                                                                           
     _,person,_,_=self.personExtractor.extract(rawimage,0.75)                     
     # cv2_imshow(person)
     if person is not None:
       r=self.detect_pose(person,self.pose_image,True,True)
     else:
       r=self.detect_pose(rawimage,self.pose_image,True,True)
     if r is None:
         return [0,0,0,0,0,0,None,None,None]

     if r.pose_landmarks is not None:
         landmarks=self.get_landmarks(r)
         # print(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility)
         # print(landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility)
     else:
         return [0,0,0,0,0,0,None,None]
     
     if dominate==1:
       lh=-1
       #lh=angle_lefthand(landmarks)
       rh=self.angle_righthand(landmarks)
       rs=self.angle_rightshouler(landmarks)
       ls=-1
       rk=self.angle_rightshouler_knee(landmarks)
       lk=-1
     elif dominate==0:
       rh=self.angle_lefthand(landmarks)
       lh=-1
       rs=self.angle_leftshouler(landmarks)
       ls=-1
       rk=self.angle_leftshouler_knee(landmarks)
       lk=-1

     lp=self.angle_leftpose(landmarks)
     rp=self.angle_rightpose(landmarks)
     ll=self.angle_leftleg(landmarks)
     rl=self.angle_rightpose(landmarks)
     #rs=angle_rightshouler(landmarks)
     #ls=angle_leftshouler(landmarks)

     if useage==0:
       dist=self.ankle_dist(landmarks)
       if name=='':
         return [lh,rh,lp,rp,ll,rl,ls,rs,lk,rk,dist]
       return [lh,rh,lp,rp,ll,rl,ls,rs,lk,rk,dist,name]
     if name=='':
         return [lh,rh,lp,rp,ll,rl,ls,rs,lk,rk,dominate]
     
     return [lh,rh,lp,rp,ll,rl,ls,rs,lk,rk,dominate,name]


 def calculate_elbow(self,knee,elbow,head):
   return self.calculate_angle(knee,elbow,head)

 def traingle_angle(self,img_path,name,dominate,useage):
      _,person,_,_=self.personExtractor.extract(img_path,0.5)                     
      if person is not None:
        # print('person extracted')
        r=self.detect_pose(person,self.pose_image,True,True)
      else:
        r=self.detect_pose(cv2.imread(img_path),self.pose_image,True,True)
      landmarks = [None, None, None]

      if r is None:
          print('r is none(Unable to extracts points)')
          return
      if r.pose_landmarks is None:
          print('r.pose_landmarks is none')
          return
      else:
          landmarks=self.get_landmarks(r)

      if dominate==1:
        wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        knee = [landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
      else:
        wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
      
      head=[landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,landmarks[self.mp_pose.PoseLandmark.NOSE.value].y]

      rankle = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
      lankle = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
      ankle=[(rankle[0]+lankle[0])/2,(rankle[1]+lankle[1])/2]    

      person_mid = [(head[0]+ankle[0])/2,(head[1]+ankle[1])/2]

      ankle_an=self.calculate_angle(wrist,ankle,head)
      wrist_an=self.calculate_angle(ankle,wrist,head)
      head_an=self.calculate_angle(wrist,head,ankle)
      person_mid_angle = self.calculate_angle(wrist,person_mid,ankle)
      
      forehand=False

      if dominate==1:        
        if wrist[0]>person_mid[0]:
          forehand=True
      else:
        if wrist[0]<person_mid[0]:
          forehand=True
      return [ankle_an,wrist_an,head_an,person_mid_angle,forehand,head] #WHY?: Returing head_pos to help classifying frame as serve using ball_position