# These functions are all intended to be accessed outside of their respective modules

from .preprocessing import preprocess_file, file_conversion
from .classification import predict_document_class
from .signaturedetection import signature_detection
from .database import validate_database, ClassificationResultTableRow, insert_record_command, retrieve_records_query
from .timehandling import get_current_time_as_POSIX_timestamp, datetime_to_POSIX_timestamp


# The top level function that triggers all server
# processing of the uploaded document
# including classification, signature detection,
# and updating the database
def process_uploaded_file(filename):
    doc_class = classify_uploaded_file(filename)
    signature_presence = find_signature(filename)

    return doc_class


# The function that classifies the uploaded file
# filename is the path to the file to be classified
# This function returns the predicted class as an int
def classify_uploaded_file(filename):
    extracted_text = preprocess_file(filename)
    doc_class = predict_document_class(extracted_text)

    return doc_class


# Facilitate all of the signature detection steps
def find_signature(filename):
    image = file_conversion(filename)
    signature_presence = signature_detection(image)

    return signature_presence