import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# def readfile(fileName):
#     with open(fileName, 'r') as file:
#         extracted_text = file.read().replace('\n', '')
#         extracted_text= str(extracted_text)
#     return extracted_text

CLASSIFICATION_MODELS_PATH = os.environ['IDENTIDOC_CLASSIFICATION_MODELS']

# Top level function that returns the classification of the document
# The text of the document is passed in as a singular string and
# the function returns the classification of the uploaded document as an int.
def predict_document_class(text):
    vectorized_data = vectorizer(text)
    classification = classifier(vectorized_data)
    return classification


def vectorizer(extracted_text):
    new_vec = TfidfVectorizer(vocabulary=pickle.load(
        open(os.path.join(CLASSIFICATION_MODELS_PATH, "vocab.pkl"), "rb")))
    vectorized_data = new_vec.fit_transform([extracted_text])
    return vectorized_data


def classifier(vectorized_data):
    loaded_model = pickle.load(open(os.path.join(CLASSIFICATION_MODELS_PATH, "model.pkl"), "rb"))
    prediction = loaded_model.predict(vectorized_data)
    return int(prediction[0])

# these would ideally be queried from database
# for demonstration purpose, we're using this for now
# def class_to_str(prediction):
#     if prediction == "1":
#        return "2021-2022 Cost of Attendance (COA) Adjusment Request"
#    elif prediction == "2":
#        return "2021-2022 Verification of Household"
#    elif prediction == "3":
#        return "2021-2022 Verification of Income Student"
#    elif prediction == "4":
#        return "OIE CPT Academic Advisor Recommendation"
#    elif prediction == "5":
#        return "OIE CPT Student Information"
#    else:
#        return "We Could not classify the document"


# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         # textFromFile= readfile(fileName)
#     else:
#         print("Use given format\n")
#         print("python3 classification.py userinput.txt\n")

# def main():
#     # fileName = sys.argv[1]
#     # extracted_text= readfile(fileName)
#     vectorized_data= vectorizer(extracted_text)
#     prediction= classifier(vectorized_data)
#     print(prediction)

# main()
