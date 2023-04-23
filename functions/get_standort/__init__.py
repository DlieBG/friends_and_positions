from shared_db import FAPDatabase
import azure.functions as func
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

        standort_benutzer = benutzer_collection.find_one({
            'loginName': id
        })

        if benutzer and standort_benutzer:
            return func.HttpResponse(
                body=json.dumps({
                    'standort': standort_benutzer['standort']
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
