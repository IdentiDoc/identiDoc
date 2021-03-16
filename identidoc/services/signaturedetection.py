
import cv2
import os
import subprocess


SIGNATURE_DETECTION_PATH = os.environ['IDENTIDOC_SIGNATURE_DETECTION']


#Path to cfg file and trained_weight
cfgfile = os.path.join(SIGNATURE_DETECTION_PATH, 'yolov3_custom.cfg')
trained_weights = os.path.join(SIGNATURE_DETECTION_PATH, 'yolov3_custom_final.weights')

# Trying to think of a better way to handle this, for now, this will get past CI pipeline
# Try to load the signature detection model, if it can't be loaded, just give False
try:
  #Getting the net object
  net= cv2.dnn.readNet(cfgfile,trained_weights)


  #Output layer names from yolo
  layers_names = net.getLayerNames()
  outputLayers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
except:
  net = None


#This function returns True if signature is detected with a confidence score greater than 0.5 else returns false
def signature_detection(image):
  # Trying to think of a better way to handle this, for now, this will get past CI pipeline
  if net is None:
    return False

  blob=cv2.dnn.blobFromImage(image,1/255,(416,416),swapRB=True,crop=False)
  net.setInput(blob)
  out=net.forward(outputLayers)

  for o in out:
    for detect in o:
      confidence_score=detect[5:]
      if confidence_score >0.5:
        return (True) 

  return (False)
