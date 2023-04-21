from flask import Flask, jsonify, request
from pymongo import MongoClient
from uuid import uuid4
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['fap_db']

benutzer_collection = db['benutzer']
benutzer_collection.create_index('loginName', unique=True)

@app.route('/FAPServer/service/fapservice/addUser', methods=['POST']) #length?
def add_user():
    data = request.get_json()
    if benutzer_collection.find_one({'loginName': data['loginName']}):
        return jsonify({'ergebnis': False, 'meldung': 'Benutzername bereits vorhanden.'})
    benutzer = {
        'loginName': data['loginName'],
        'passwort': data['passwort']['passwort'],
        'vorname': data['vorname'],
        'nachname': data['nachname'],
        'strasse': data['strasse'],
        'plz': data['plz'],
        'ort': data['ort'],
        'land': data['land'],
        'telefon': data['telefon'],
        'email': data['email']
    }
    benutzer_collection.insert_one(benutzer)
    return jsonify({'ergebnis': True, 'meldung': ''})

@app.route('/FAPServer/service/fapservice/checkLoginName') #length?
def check_login_name():
    id = request.args.get('id')
    if benutzer_collection.find_one({'loginName': {'$regex': '^' + id}}):
        return jsonify({'ergebnis': True})
    else:
        return jsonify({'ergebnis': False})

@app.route('/FAPServer/service/fapservice/login', methods=['POST'])
def login():
    data = request.get_json()
    benutzer = benutzer_collection.find_one({'loginName': data['loginName'], 'passwort': data['passwort']['passwort']})
    if benutzer:
        session_id = str(uuid4())
        benutzer_collection.update_one({'_id': benutzer['_id']}, {'$set': {'session_id': session_id}})
        return jsonify({'sessionID': session_id})
    else:
        return jsonify({'ergebnis': False})

@app.route('/FAPServer/service/fapservice/logout', methods=['POST'])
def logout():
    data = request.get_json()
    benutzer = benutzer_collection.find_one({'loginName': data['loginName'], 'session_id': data['sitzung']})
    if benutzer:
        benutzer_collection.update_one({'_id': benutzer['_id']}, {'$unset': {'session_id': ""}})
        return jsonify({'ergebnis': True})
    else:
        return jsonify({'ergebnis': False})

@app.route('/FAPServer/service/fapservice/setStandort', methods=['PUT'])
def set_standort():
    data = request.get_json()
    benutzer = benutzer_collection.find_one({'loginName': data['loginName'], 'session_id': data['sitzung']})
    if benutzer:
        standort = data['standort']
        benutzer_collection.update_one({'_id': benutzer['_id']}, {'$set': {'standort': standort}})
        return jsonify({'ergebnis': True})
    else:
        return jsonify({'ergebnis': False})

@app.route('/FAPServer/service/fapservice/getStandort', methods=['GET'])
def get_standort():
    login_name = request.args.get('login')
    session_id = request.args.get('session')
    id = request.args.get('id')
    benutzer = benutzer_collection.find_one({'loginName': login_name, 'session_id': session_id})
    if benutzer and benutzer['loginName'] == id:
        standort = benutzer.get('standort')
        if standort:
            return jsonify(standort)
    return jsonify({'ergebnis': False})

@app.route('/FAPServer/service/fapservice/getBenutzer', methods=['GET'])
def get_benutzer():
    login_name = request.args.get('login')
    session_id = request.args.get('session')
    benutzer = benutzer_collection.find_one({'loginName': login_name, 'session_id': session_id})
    if benutzer:
        benutzerliste = benutzer_collection.find({}, {'loginName': 1, 'vorname': 1, 'nachname': 1})
        return jsonify({'benutzerliste': [{k:v for k, v in x.items() if k != '_id'} for x in benutzerliste]})
    return jsonify({'ergebnis': False})

@app.route('/FAPServer/service/fapservice/getStandortPerAdresse', methods=['GET'])
def get_standort_per_adresse():
    land = request.args.get('land')
    plz = request.args.get('plz')
    ort = request.args.get('ort')
    strasse = request.args.get('strasse')
    geolocator = Nominatim(user_agent="fap-service")
    location = geolocator.geocode(f"{strasse}, {plz} {ort}, {land}")
    if location:
        return jsonify({'breitengrad': location.latitude, 'laengengrad': location.longitude})
    return jsonify({'ergebnis': False})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
