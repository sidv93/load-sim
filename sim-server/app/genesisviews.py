from flask import render_template, request
from json import dumps

from app import app

@app.route('/genesis')
def app_home():
    return render_template('genesis.html')

@app.route('/genesis/app')
def app_root():
    return render_template('gapp.html')