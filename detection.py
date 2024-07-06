import cv2
import mediapipe as mp
import numpy as np

mp_drawing=mp.solutions.drawing_utils
mp_pose=mp.solutions.pose

import numpy as np

def calculate_angle(a, b, c=0):
    """
    Calculates the angle between two points, a and b, in degrees.

    Parameters:
    a (array-like): The coordinates of point a.
    b (array-like): The coordinates of point b.
    c (array-like, optional): The coordinates of point c. Defaults to [0, 0].

    Returns:
    float: The angle between points a and b in degrees.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

# Inline documentation for the project
"""
This project is focused on fitness detection. The `detection.py` module contains functions for calculating angles between points.
The `calculate_angle` function calculates the angle between two points, a and b, in degrees. It takes in the coordinates of the points as input and returns the angle.
"""
def calculate_angle(a,b,c=0):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)

    radians=np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
 
  
    return angle

cap=cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    while cap.isOpened(): 
     ret,frame=cap.read()

     image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
     image.flags.writeable=False

     results=pose.process(image)

     image.flags.writeable=True
     image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
     try:
         landmarks=results.pose_landmarks.landmark
         Lshoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
         Lelbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
         Lwrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
         Lhip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
         Lknee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
         Lankle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        
        
       
         Rshoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
         Relbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
         Rwrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
         Rhip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
         Rknee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
         Rankle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

         angle1=(180-calculate_angle(Lshoulder,Lelbow).astype(int))
         print('angle1-',angle1)
        
         cv2.putText(image,str(angle1),
                     tuple(np.multiply(Lshoulder,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
         angle2=calculate_angle(Rshoulder,Relbow).astype(int)
         print('angle2-',angle2)
         cv2.putText(image,str(angle2),
                     tuple(np.multiply(Rshoulder,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
        

         angle3=calculate_angle(Lhip,Lknee).astype(int)
         print('angle3-',angle3)
         cv2.putText(image,str(angle3),
                     tuple(np.multiply(Lankle,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
         
         
         angle4=90+calculate_angle(Rhip,Rknee).astype(int)
         print('angle4-',angle4)
         cv2.putText(image,str(angle4),
                     tuple(np.multiply(Rknee,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
         
         if angle1>20 or angle2>20 :
             alert='please ,raise your both hands upwards '
             
             cv2.putText(image,alert,(24,25),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255),1,cv2.LINE_AA)

         elif angle4>120 :
              alert='please,bend your knee.'
              cv2.putText(image,alert,(24,25),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255),1,cv2.LINE_AA)

         else :
              alert='perfect,your are doing great.'
              cv2.putText(image,alert,(24,25),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255),1,cv2.LINE_AA)
      
       
     except:
         pass

    

             
     mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                               mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                               mp_drawing.DrawingSpec(color=(255,255,255),thickness=4,circle_radius=3))

    
     cv2.imshow('frame',image)
     
     if cv2.waitKey(10) & 0xff == ord('q'):
            break
   

cap.release()
cv2.destroyAllWindows()


