import azure.functions as func
from db import FAPDatabase
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    with FAPDatabase('benutzer') as benutzer_collection:
        login_name = req.params.get('login')
        session_id = req.params.get('session')
        id = req.params.get('id')

        benutzer = benutzer_collection.find_one({
            'loginName': login_name,
            'session_id': session_id
        })

        if benutzer:
            benutzerliste = benutzer_collection.find(
                {},
                {
                    '_id': 0,
                    'loginName': 1,
                    'vorname': 1,
                    'nachname': 1
                }
            )

            return func.HttpResponse(
                body=json.dumps({
                    'benutzerliste': list(benutzerliste)
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
