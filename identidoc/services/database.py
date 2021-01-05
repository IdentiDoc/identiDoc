# An object that is equivalent to a database record
#
# A list of ClassificaitonResultTableRows will be returned from a database query
# A ClassificationResultTableRow will need to be created to insert a database record
class ClassificationResultTableRow(object):
    # filename - raw filename from identidoc with timestamp
    # Example: 04122020164952378563.21-22_Verification_of_Household.pdf
    #
    # classification - an integer 0 - 5 inclusive
    # 1 - 5 is a classified document
    # 0 is a non-classified document
    # 
    # has_signature - True or False
    def __init__(self, filename, classification, has_signature):
        try:
            # Ensure that the classification field is an integer and falls within the acceptable interval
            assert isinstance(classification, int)
            assert 0 <= classification and classification <= 5

            assert isinstance(has_signature, bool)

            # We're going to assume that the filename has already been validated/created through the api,
            # which it should be. Please don't abuse this privileges
            split_filename = filename.split(".", 1)
            assert len(split_filename) == 2

            self.timestamp = split_filename[0]
            self.filename = split_filename[1]
            self.classification = classification
            self.has_signature = has_signature


        except AssertionError:
            self = None
