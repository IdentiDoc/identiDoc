import cv2
import pytesseract
import json
import subprocess
import sys
import os


# This function serves as a wrapper function that handles all preprocessing for the Sprint 4 demonstration
# TODO - Add another level of wrapper functions in the __init__.py file to handle classification as well
# arguments - filename: the path to the input file
# returns - filepath to .txt of extracted text that will be downloaded for the Sprint 4 demonstration.
def preprocess_file(filename):
    # .txt files are still valid. They probably shouldn't be?
    if filename.lower().endswith('.txt'):
        return filename

    image = file_conversion(filename)
    processed_image = image_pre_processing(image)
    extracted_text = tesseract_text_extraction(processed_image)

    # This returns the abosule filepath to the extracted text.
    return save_text_to_file(extracted_text)




# This function performs pre-processiong on the image file provided
def image_pre_processing(image):
    #convert image color to gray
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #convert the grayscaled image to binary image
    final_image= cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return final_image


# This function extracts text from the pre-processed image
def tesseract_text_extraction(image):
    tesseract_config = r'--oem 3 --psm 6'
    #feeding the image to the tessercat
    extracted_text= pytesseract.image_to_string(image, output_type=pytesseract.Output.DICT, config=tesseract_config, lang='eng')
    return extracted_text


#This function writes the extracted text to a file
def save_text_to_file(extracted_text):
    with open('UTA_form.txt', 'w', newline="") as file:
        #file.write(json.dumps(extracted_text))
        file.write(extracted_text['text'])  # Made this adjustment just for now
    
    return os.path.abspath('UTA_form.txt')


#This function converts the input file to .png
def file_conversion(fileName):
    if fileName.lower().endswith(('.png','.jpg','.jpeg')):
        image = cv2.imread(fileName)
    elif fileName.lower().endswith('.pdf'):
        subprocess.call(["pdftoppm", "-png", fileName, "temp"])
        image = cv2.imread("temp-1.png")
    elif fileName.lower().endswith('.heic'):
        subprocess.call(["heif-convert", fileName, "temp.png"])
        image = cv2.imread("temp.png")
    return image


if __name__ == "__main__":
    if len(sys.argv) == 2:
        #convert
        fileName = sys.argv[1]
        #reading image
        init_image = file_conversion(fileName)
        #call pre-processing function
        processed_image = image_pre_processing(init_image)
        # call text-extraction function
        text_extracted = tesseract_text_extraction(processed_image) 
        #call save to a file
        save_text_to_file(text_extracted)
    else:
        print("Use given format\n")
        print("python3 file.py fileName.extension\n")

