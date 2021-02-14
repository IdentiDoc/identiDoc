import pickle
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

def readfile(fileName):
    with open(fileName, 'r') as file:
        extracted_text = file.read().replace('\n', '')
        extracted_text= str(extracted_text)
    return extracted_text
	
def vectorizer(extracted_text):
    new_vec=TfidfVectorizer(vocabulary=pickle.load(open("classification_model/vocab.pkl","rb")))
    vectorized_data=new_vec.fit_transform([extracted_text])
    return vectorized_data

def classifier(vectorized_data):
    loaded_model=pickle.load(open("classification_model/model.pkl","rb"))
    prediction=loaded_model.predict(vectorized_data)
    return prediction

# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         # textFromFile= readfile(fileName)
#     else:
#         print("Use given format\n")
#         print("python3 classification.py userinput.txt\n")

def main():
    fileName = sys.argv[1]
    extracted_text= readfile(fileName)
    vectorized_data= vectorizer(extracted_text)
    prediction= classifier(vectorized_data)
    print(prediction)

main()
