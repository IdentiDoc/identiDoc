# This is going to mimmic the backend system right now...


class ClassificationResultQuery:
    def __init__(self, date):
        self.date = date

# "Getting" the classification results that were classified on the given date
def GetClassificationQueryResults(query):
    return "These are the classification results from " + query.date