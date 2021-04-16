import cv2
import pytesseract
import re
import subprocess
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

stopwords = set(stopwords.words("english"))
regex_pat = re.compile(r'[^a-zA-Z\s]', flags=re.IGNORECASE)

TEMP_PATH = os.environ['IDENTIDOC_TEMP_PATH']

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

# This function serves as a wrapper function that handles all initial image preprocessing
# arguments - filepath: the path to the input file
# returns - the text extracted from the input file in the correct form to be classified


def preprocess_file(filepath):
    image = file_conversion(filepath)
    rotated_image = rotate_image(image)
    processed_image = image_pre_processing(rotated_image)
    extracted_text = tesseract_text_extraction(processed_image)

    extracted_text = extracted_text.replace('\n', ' ')
    
    # remove stopwords,lemmatize and convert to  lowercase
    extracted_text = remove_stopwords(extracted_text)

    # This returns the extracted text in the form that is classifiable

    return extracted_text


# This function rotates the image correctly
# Input is a cv2 image that may or may not be oriented correctly
# Output is a cv2 image that is oriented correctly by tesseract
def rotate_image(image):
    try:
        orig_image_osd = pytesseract.image_to_osd(image)
        image_rotation_angle = re.search(
            '(?<=Rotate: )\d+', orig_image_osd).group(0)
    except:
        return image

    correctly_oriented_image = image

    if image_rotation_angle == '0':
        correctly_oriented_image = image
    elif image_rotation_angle == '90':
        correctly_oriented_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif image_rotation_angle == '180':
        correctly_oriented_image = cv2.rotate(image, cv2.ROTATE_180)
    elif image_rotation_angle == '270':
        correctly_oriented_image = cv2.rotate(
            image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return correctly_oriented_image


# This function performs pre-processiong on the image file provided
def image_pre_processing(image):
    # convert image color to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # convert the grayscaled image to binary image
    final_image = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return final_image


def remove_stopwords(sentence):
    lemmatizer = WordNetLemmatizer()
    processed_sent = ''
    temp_sent = word_tokenize(sentence)
    for word in temp_sent:
        word = word.lower()
        word = lemmatizer.lemmatize(word)
        if word not in stopwords:
            if not regex_pat.search(word):
                processed_sent = processed_sent+" "+word
    return processed_sent


# This function extracts text from the pre-processed image
def tesseract_text_extraction(image):
    tesseract_config = r'-c tessedit_char_whitelist=" -.@/()%:\',?!0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" --oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(
        image, output_type=pytesseract.Output.STRING, config=tesseract_config, lang='eng')
    return str(extracted_text)


# This function converts the input file to .png
def file_conversion(filepath):
    if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = cv2.imread(filepath)
    elif filepath.lower().endswith('.pdf'):
        subprocess.call(["pdftoppm", "-png", filepath,
                         os.path.join(TEMP_PATH, "temp")])
        image = cv2.imread(os.path.join(TEMP_PATH, "temp-1.png"))
    elif filepath.lower().endswith('.heic'):
        subprocess.call(["heif-convert", filepath,
                         os.path.join(TEMP_PATH, "temp.png")])
        image = cv2.imread(os.path.join(TEMP_PATH, "temp.png"))
    return image
