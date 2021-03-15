# These functions are all intended to be accessed outside of their respective modules
# SOME OF THEM ARE NOT NEEDED HERE, BUT ARE USED IN OTHER MODULES THAT IMPORT identidoc.services
# DON'T TOUCH PLEASE

from .preprocessing import preprocess_file, file_conversion
from .classification import predict_document_class
from .signaturedetection import signature_detection
from .database import validate_database, ClassificationResultTableRow, insert_record_command, retrieve_records_query
from .timehandling import get_current_time_as_POSIX_timestamp, datetime_to_POSIX_timestamp


# The top level function that triggers all server
# processing of the uploaded document
# including classification, signature detection,
# and updating the database
def process_uploaded_file(filepath):
    # Get the classification of the document
    doc_class = classify_uploaded_file(filepath)

    # Don't look for a signature if the document is not recognized
    if doc_class == 0:
        signature_presence = False
    else:
        signature_presence = find_signature(filepath)

    # Database only stores the filename - We know where the file is stored on the server
    filename = filepath.split('/')[-1]

    # Update the database with a classification result
    database_result = update_database(filename, doc_class, signature_presence)

    # Error with the database record
    if database_result == -1:
        return None, None

    return doc_class, signature_presence


# The function that classifies the uploaded file
# filename is the path to the file to be classified
# This function returns the predicted class as an int
def classify_uploaded_file(filepath):
    extracted_text = preprocess_file(filepath)
    doc_class = predict_document_class(extracted_text)

    return doc_class


# Facilitate all of the signature detection steps
def find_signature(filepath):
    image = file_conversion(filepath)
    signature_presence = signature_detection(image)

    return signature_presence


# Update Database
def update_database(filename, classification, signature_presence):
    record = ClassificationResultTableRow(
        filename, classification, signature_presence)

    return insert_record_command(record)
