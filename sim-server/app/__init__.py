from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

from app import views
from app import systemroutes
from app import genesisroutes
from app import genesisviews

