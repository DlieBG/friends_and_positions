from pymongo import MongoClient
import azure.functions as func
import json, os

def main(req: func.HttpRequest) -> func.HttpResponse:
    benutzer_collection = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017')).get_database('friends_and_positions').get_collection('benutzer')
    benutzer_collection.create_index('loginName', unique=True)
    
    body = req.get_json()

    if benutzer_collection.find_one({
        'loginName': body['loginName']
    }):
        return func.HttpResponse(
            body=json.dumps({
                'ergebnis': False,
                'meldung': 'LoginName bereits vorhanden'
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
