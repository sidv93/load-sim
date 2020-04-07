import requests
import websocket
import json

import multiprocessing
import subprocess
import threading
import time
import uuid
import os
import signal

from .genesisuser import GenesisUser;
from .genesismcs import MCS;
from app import app

class Flight():

    def __init__(self, server, mcs, user, home):
        self.baseurl = server
        self.mcs = mcs
        self.user = user
        self.home = home

        self.vehicle_id = f'SimulatedVehicle-{str(uuid.uuid4())[:8]}'

        self.registrationInfo = {}
        self.telemetryStream = None
        self.videoStream = None
        self.ffmpegPID = None

    def mcs(self):
        return self.mcs

    def flightId(self):
        return self.registrationInfo['flightId']

    def socketURL(self):
        return self.registrationInfo['socketServer']
    
    def videoURL(self):
        return self.registrationInfo['videoServer']

    def register(self, plan=None):
        flighturl = f'{self.baseurl}/api/v1.0/flight/plan'
        data = {
            'auth_token': self.user.token(),
            'client_id': self.mcs.clientId(),
            'mcs_id': self.mcs.mcsId(),
            'vehicle_id': self.vehicle_id,
            'latitude': self.home['latitude'] if self.home else None,
            'longitude': self.home['longitude'] if self.home else None,
            'flight_status': 'Running',
            'protocol': 'MAVLINK',
            'flight_plan': json.dumps(plan)
        }
        res = requests.post(url=flighturl, data=data)
        self.registrationInfo = res.json()['data']
        print(f"{self.registrationInfo['videoServer']}/{self.user.token()}/640/480")

    def start(self):
        self.startTelemetry()
        self.startVideo()
  
    def stop(self):
        self.telemetryStream.terminate() if self.telemetryStream else None
        self.videoStream.terminate() if self.videoStream else None
        os.kill(self.ffmpegPID, signal.SIGTERM) if self.ffmpegPID else None

    def startTelemetry(self):
        options = {
            'auth_token': self.user.token(),
            'client_id': self.mcs.clientId(),
            'vehicle_id': self.vehicle_id,
            'mcs_id': self.mcs.mcsId(),
            'flight_id': self.flightId()
        }
        self.telemetryStream = multiprocessing.Process(target=startWS, args=(self.socketURL(), options, self.home,), name=f'Tele-{self.flightId()}')
        self.telemetryStream.start()

    def startVideo(self):
        video_url = f'{self.registrationInfo["videoServer"]}/{self.user.token()}/640/480'
        q = multiprocessing.Queue()
        self.videoStream = multiprocessing.Process(target=publish_video, args=(video_url,q,), name=f'Video-{self.flightId()}')
        self.videoStream.start()
        self.ffmpegPID = q.get()
        
def startWS(url, options, home):
    ws = websocket.WebSocketApp(url)
    ws.home = home
    ws.flightTime = 0
    ws.on_open = lambda ws: ws.send(ws.send(json.dumps(options)))
    ws.on_message = handshake_response_recv 
    ws.run_forever()

def handshake_response_recv(ws, msg):
    while True:
        publish_telemetry(ws)
        time.sleep(1)

def publish_telemetry(ws):
    ws.send(json.dumps({
        'latitude': ws.home['latitude'],
        'longitude': ws.home['longitude'],
        'autopilotModeName': 'NAV',
        'targetWaypointNumber': 2,
        'pilot': 'simulator',
        'airspeed': 0,
        'videoUploadSpeed': 2,
        'zoomLevel': 1,
        'heading': 297.92,
        'fov': 46,
        'flightTime': ws.flightTime,
        'autopilotMode': 3,
        'barometricAltitude': 99.53,
        'timeElapsed': ws.flightTime,
        'gpsSpeed': 10,
        'batteryStatus': 98,
        'armedStatus': 1,
        'genesisCommandEnabled': False
    }))
    ws.home = {
        'latitude': ws.home['latitude'] + 0.00001,
        'longitude': ws.home['longitude'] + 0.00001,
    }
    ws.flightTime += 1
    
def publish_video(video_url, q):
    ffmpeg_options = f'ffmpeg -i {app.config["VIDEO_URL"]} -f mpeg1video -vf scale=640:480 -b 200k -r 20'
    options = f"{ffmpeg_options} {video_url}".split()
    pid = subprocess.Popen(options).pid
    q.put(pid)