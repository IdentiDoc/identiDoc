
import cv2
import os
import subprocess


SIGNATURE_DETECTION_PATH = os.environ['IDENTIDOC_SIGNATURE_DETECTION']


#Path to cfg file and trained_weight
cfgfile = os.path.join(SIGNATURE_DETECTION_PATH, 'yolov3_custom.cfg')
trained_weights = os.path.join(SIGNATURE_DETECTION_PATH, 'yolov3_custom_final.weights')


#Getting the net object
net= cv2.dnn.readNet(cfgfile,trained_weights)


#Output layer names from yolo
layers_names = net.getLayerNames()
outputLayers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]


#This function returns True if signature is detected with a confidence score greater than 0.5 else returns false
def signature_detection(image):

  blob=cv2.dnn.blobFromImage(image,1/255,(416,416),swapRB=True,crop=False)
  net.setInput(blob)
  out=net.forward(outputLayers)

  for o in out:
    for detect in o:
      confidence_score=detect[5:]
      if confidence_score >0.5:
        return (True) 

  return (False)
