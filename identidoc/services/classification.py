import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer


CLASSIFICATION_MODELS_PATH = os.environ['IDENTIDOC_CLASSIFICATION_MODELS']

# Top level function that returns the classification of the document
# The text of the document is passed in as a singular string and
# the function returns the classification of the uploaded document as an int.
def predict_document_class(text):
    #more preprocessing

    vectorized_data = vectorizer(text)
    classification = classifier(vectorized_data)
    return classification


def vectorizer(extracted_text):
    new_vec = CountVectorizer(vocabulary=pickle.load(
        open(os.path.join(CLASSIFICATION_MODELS_PATH, "vocab.pkl"), "rb")))
    vectorized_data = new_vec.fit_transform([extracted_text])
    return vectorized_data


def classifier(vectorized_data):
    prediction_threshold=0.8
    loaded_model = pickle.load(open(os.path.join(CLASSIFICATION_MODELS_PATH, "model.pkl"), "rb"))
    prediction = loaded_model.predict_proba(vectorized_data)
    predicted =prediction[0]
    selected_class=0
    max_prob=0

    for i,predictions in enumerate(predicted):
        if predictions>prediction_threshold:
            if predictions>max_prob:
                max_prob=predictions
                selected_class=i

    return selected_class
