import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer


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
