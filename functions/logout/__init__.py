import azure.functions as func
from db import FAPDatabase
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    with FAPDatabase('benutzer') as benutzer_collection:
        body = req.get_json()

        benutzer = benutzer_collection.find_one({
            'loginName': body['loginName'],
            'session_id': body['sitzung']
        })

        if benutzer:
            benutzer_collection.update_one(
                {
                    '_id': benutzer['_id']
                },
                {
                    '$unset': {
                        'session_id': ''
                    }
                }
            )

            return func.HttpResponse(
                body=json.dumps({
                    'ergebnis': True
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