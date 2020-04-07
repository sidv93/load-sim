def plan_from_home(home):
    plan = {
        'flightMode': 'Once',
        'waypoints': [
            {
                'index': 0,
                'type': 'home',
                'latitude': home['latitude'],
                'longitude': home['longitude'],
                'altitude': 0
            },
            {
                'index': 1,
                'type': 'takeoff',
                'latitude': home['latitude'],
                'longitude': home['longitude'],
                'altitude': 100,
                'data': {
                    'loiterType': '',
                    'value': 0
                }
            },
            {
                'index': 2,
                'type': 'nav',
                'latitude': home['latitude'] + 0.01,
                'longitude': home['longitude'] + 0.01,
                'altitude': 100,
                'data': {
                    'loiterType': '',
                    'value': 0
                }
            }
        ]
    }
    return plan
