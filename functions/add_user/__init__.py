import azure.functions as func
from db import FAPDatabase
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    with FAPDatabase('benutzer') as benutzer_collection:
        body = req.get_json()

        if benutzer_collection.find_one({
            'loginName': body['loginName']
        }):
            return func.HttpResponse(
                body=json.dumps({
                    'ergebnis': False,
                    'meldung': 'Benutzername bereits vorhanden.'
                }),
                status_code=200,
                mimetype='applicatoin/json',
                charset='utf-8'
            )

        benutzer_collection.insert_one({
            'loginName': body['loginName'],
            'passwort': body['passwort']['passwort'],
            'vorname': body['vorname'],
            'nachname': body['nachname'],
            'strasse': body['strasse'],
            'plz': body['plz'],
            'ort': body['ort'],
            'land': body['land'],
            'telefon': body['telefon'],
            'email': body['email']
        })

        return func.HttpResponse(
            body=json.dumps({
                'ergebnis': True,
                'meldung': ''
            }),
            status_code=200,
            mimetype='applicatoin/json',
            charset='utf-8'
        )
