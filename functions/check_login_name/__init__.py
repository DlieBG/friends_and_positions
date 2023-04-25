from pymongo import MongoClient
import azure.functions as func
import json, os


def main(req: func.HttpRequest) -> func.HttpResponse:
    benutzer_collection = MongoClient(os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017')).get_database('friends_and_positions').get_collection('benutzer')
    
    id = req.params.get('id')

    if benutzer_collection.find_one({
        'loginName': {
            '$regex': f'^{id}'
        }
    }):
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
