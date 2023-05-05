from pymongo import MongoClient
import azure.functions as func
import json, os


def main(req: func.HttpRequest) -> func.HttpResponse:
    benutzer_collection = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017')).get_database('friends_and_positions').get_collection('benutzer')
    try:
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
    except:
        pass
    return func.HttpResponse(
            body=json.dumps({
                'ergebnis': False,
                'meldung': '400'
            }),
            status_code=200,
            mimetype='application/json',
            charset='utf-8'
        )
