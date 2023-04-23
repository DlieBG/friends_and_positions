from geopy.geocoders import Nominatim
import azure.functions as func
from db import FAPDatabase
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    with FAPDatabase('benutzer') as benutzer_collection:
        land = req.params.get('land')
        plz = req.params.get('plz')
        ort = req.params.get('ort')
        strasse = req.params.get('strasse')

        geolocator = Nominatim(user_agent='fap_function')
        location = geolocator.geocode(f'{strasse}, {plz} {ort}, {land}')

        if location:
            return func.HttpResponse(
                body=json.dumps({
                    'breitengrad': location.latitude,
                    'laengengrad': location.longitude
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
