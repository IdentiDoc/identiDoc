import pickle
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

def readfile(fileName):
    with open(fileName, 'r') as file:
        extracted_text = file.read().replace('\n', '')
        extracted_text= str(data)
    return extracted_text
	
# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         # textFromFile= readfile(fileName)
#     else:
#         print("Use given format\n")
#         print("python3 classification.py userinput.txt\n")

def main():
    fileName = sys.argv[1]
    extracted_text= readfile(fileName)

main()
