from pymongo import MongoClient
import azure.functions as func
from uuid import uuid4
import json, os


def main(req: func.HttpRequest) -> func.HttpResponse:
    benutzer_collection = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017')).get_database('friends_and_positions').get_collection('benutzer')

    body = req.get_json()

    benutzer = benutzer_collection.find_one({
        'loginName': body['loginName'],
        'passwort': body['passwort']['passwort']
    })

    if benutzer:
        session_id = str(uuid4())

        benutzer_collection.update_one(
            {
                '_id': benutzer['_id']
            },
            {
                '$set': {
                    'session_id': session_id
                }
            }
        )

        return func.HttpResponse(
            body=json.dumps({
                'sessionID': session_id
            }),
            status_code=200,
            mimetype='applicatoin/json',
            charset='utf-8'
        )

    return func.HttpResponse(
        body=json.dumps({
            'ergebnis': False
        }),
        status_code=200,
        mimetype='applicatoin/json',
        charset='utf-8'
    )
