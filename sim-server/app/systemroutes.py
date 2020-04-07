from flask import request
from json import dumps
from app import app

import psutil

@app.route('/system/stats', methods=['GET'])
def get_system_stats():
    return {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory()._asdict()['percent']
    }