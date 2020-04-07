from os import environ

DEBUG = True
VIDEO_URL = 'udp://@224.10.10.10:15004' if not environ.get('VIDEO_URL') else environ.get('VIDEO_URL')
