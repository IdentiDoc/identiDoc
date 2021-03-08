# RESTful API Resource for query

import json
from datetime import datetime
from identidoc.services import retrieve_records_query
from flask import jsonify
from flask_restful import Resource


class QueryResult(Resource):
    def get(self, UI_date, UI_classification, UI_signature):
        classification_date, classification, has_signature = self.prepare_query(
            UI_date, UI_classification, UI_signature)
        results = retrieve_records_query(
            classification_date, classification, has_signature)

        return jsonify(
            number=len(results),
            results=[result.toJSON() for result in results]
        )

    # This function takes the raw data collected from the UI and
    # processes it into the necessary form to perform the query

    @staticmethod
    def prepare_query(raw_date, raw_classification, raw_signature):
        if raw_date == 'None':
            date = None
        else:
            date = datetime.strptime(raw_date, '%Y-%m-%d')

        if raw_classification == '-1':
            classification = None
        else:
            classification = int(raw_classification)

        if raw_signature == '-1':
            signature = None
        elif raw_signature == '0':
            signature = False
        else:
            signature = True

        return date, classification, signature
