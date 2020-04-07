from flask import redirect, request
from json import dumps

from app import app
# from .utils import TelemetryWorker

# workers = []

@app.route('/')
def index():
    return redirect('/genesis')

# @app.route('/flights')
# def get_sims():
#     data = list(map(lambda w: w.id(), workers))
#     return dumps(data)

# @app.route('/flights/<flightid>', methods=['GET'])
# def get_specific_sim(flightid):
#     worker = next((w for w in workers if w.id() == flightid), None)
#     return worker.data() if worker else "No such sim"

# @app.route('/flights', methods=['POST'])
# def add_sim():
#     worker = TelemetryWorker(id=f"W-{len(workers)}")
#     worker.start()
#     workers.append(worker)
#     return "Sim added"

# @app.route('/flights', methods=['DELETE'])
# def remove_sim():
#     worker = workers.pop() if len(workers) > 0 else None
#     worker.stop() and worker.join() if worker else None
#     return "Sim removed" if len(workers) else "No sims available"

# @app.route('/flights/<flightid>', methods=['DELETE'])
# def remove_specific_sim(flightid):
#     worker = next((w for w in workers if w.id() == flightid), None)
#     workers.remove(worker) if worker else None
#     worker.stop() and worker.join() if worker else None
#     return "Sim removed" if worker else "No such sim"

