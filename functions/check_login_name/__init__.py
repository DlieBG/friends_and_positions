from shared_db import FAPDatabase
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    with FAPDatabase('benutzer') as benutzer_collection:
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
