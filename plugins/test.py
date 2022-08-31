import sys
import cv2
from Helpers.person_extraction import PersonExtraction

pe = PersonExtraction("../downloaded_models/yolo.h5")
racket,person,racket_mid,person_mid = pe.extract("../ref_images/tennis/backhand/1.png",0.75)
cv2.imshow("person",person)
cv2.waitKey()
cv2.imshow("racket",racket)
cv2.waitKey()
