from pymongo import MongoClient
import azure.functions as func
import json, os


def main(req: func.HttpRequest) -> func.HttpResponse:
    benutzer_collection = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017')).get_database('friends_and_positions').get_collection('benutzer')

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
            mimetype='application/json',
            charset='utf-8'
        )

    return func.HttpResponse(
        body=json.dumps({
            'ergebnis': False
        }),
        status_code=200,
        mimetype='application/json',
        charset='utf-8'
    )
