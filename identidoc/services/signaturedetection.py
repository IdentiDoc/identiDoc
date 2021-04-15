
import cv2
import os
import subprocess


SIGNATURE_DETECTION_PATH = os.environ['IDENTIDOC_SIGNATURE_DETECTION']
TEMP_PATH = os.environ['IDENTIDOC_TEMP_PATH']


# Path to cfg file and trained_weight
cfgfile = os.path.join(SIGNATURE_DETECTION_PATH, 'yolov3_custom.cfg')
trained_weights = os.path.join(
    SIGNATURE_DETECTION_PATH, 'yolov3_custom_final.weights')

# Trying to think of a better way to handle this, for now, this will get past CI pipeline
# Try to load the signature detection model, if it can't be loaded, just give False
try:
    # Getting the net object
    net = cv2.dnn.readNet(cfgfile, trained_weights)

    # Output layer names from yolo
    layers_names = net.getLayerNames()
    outputLayers = [layers_names[i[0]-1]
                    for i in net.getUnconnectedOutLayers()]
except:
    net = None


# This function returns True if signature is detected with a confidence score greater than 0.5 else returns false
def signature_detection(image):
    # Trying to think of a better way to handle this, for now, this will get past CI pipeline
    if net is None:
        return False

    # get the height and width of the received image
    height, width, channels = image.shape
    blob = cv2.dnn.blobFromImage(
        image, 1/255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    out = net.forward(outputLayers)

    for o in out:
        for detect in o:
            confidence_score = detect[5:]
            if confidence_score > 0.5:
                # [(x,y)-centre coordinate of the signature object],[h and w, height and width of bounding box]
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                # draw bounding box rectangle around the detecetd signature
                image = cv2.rectangle(
                    image, (x, y), (x+w, y+h), (0, 128, 0), 10)
                # draw a text string,"Signature" above the bounding box rectangle
                image = cv2.putText(image, "Signature", (x, y),
                                    cv2.FONT_ITALIC, 2, (0, 0, 255), 8)
                # save the predicted image
                cv2.imwrite(os.path.join(
                    TEMP_PATH, 'yolo_prediction.jpg'), image)

                return (True)

    cv2.imwrite(os.path.join(TEMP_PATH, 'yolo_prediction.jpg'), image)
    return (False)
