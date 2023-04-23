import azure.functions as func
from db import FAPDatabase
from uuid import uuid4
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    with FAPDatabase('benutzer') as benutzer_collection:
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
