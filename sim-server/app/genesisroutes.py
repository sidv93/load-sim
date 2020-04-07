from flask import render_template, request
from json import dumps

from app import app
from .utils import GAPI

gapi_store = {}

CLIENTID = 'LoadSimulator';
MCSID = 'LoadSimMCS';

@app.route('/genesis/api/auth', methods=['GET'])
def is_genesis_auth_done():
    return {
        'server': "" if not 'gapi' in gapi_store.keys() else gapi_store['gapi'].baseURL(),
        'username': "" if not 'gapi' in gapi_store.keys() else gapi_store['gapi'].username(),
        'flights': [] if not 'gapi' in gapi_store.keys() else gapi_store['gapi'].flights(),
    }

@app.route('/genesis/api/auth', methods=['POST'])
def genesis_auth():
    if not request.form \
        or not request.form['server'] \
        or not request.form['username'] \
        or not request.form['password']:
        return is_genesis_auth_done()

    if not 'gapi' in gapi_store.keys():
        server = request.form['server']
        username = request.form['username']
        password = request.form['password']
        gapi = GAPI(server=server, username=username, password=password, clientId=CLIENTID, mcsId=MCSID)
        gapi_store['gapi'] = gapi
    
    return {
        'server': gapi_store['gapi'].baseURL(),
        'username': gapi_store['gapi'].username(),
        'flights': gapi_store['gapi'].flights()
    }

@app.route('/genesis/api/auth', methods=['DELETE'])
def genesis_unauth():
    global gapi_store
    if not 'gapi' in gapi_store.keys():
        return is_genesis_auth_done()

    gapi = gapi_store['gapi']

    while len(gapi.flights()) > 0:
        gapi.removeFlight()

    gapi.unauthenticate()

    gapi_store = {}
    return is_genesis_auth_done()

@app.route('/genesis/api/flights', methods=['POST'])
def start_genesis_flight():
    if not 'gapi' in gapi_store.keys():
        return is_genesis_auth_done()

    gapi = gapi_store['gapi']
    flight_id = gapi.startFlight()
    return {
        'flightId': flight_id
    }

@app.route('/genesis/api/flights/scale/<int:count>', methods=['POST'])
def scale_genesis_flights(count):
    if not 'gapi' in gapi_store.keys():
        return is_genesis_auth_done()

    gapi = gapi_store['gapi']
    offset =  count - len(gapi.flights())

    if offset > 0:
        while len(gapi.flights()) < count:
            gapi.startFlight()
    elif offset < 0:
        while len(gapi.flights()) > count:
            gapi.removeFlight()

    return dumps(gapi.flights())
