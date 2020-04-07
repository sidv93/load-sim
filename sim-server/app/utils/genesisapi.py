import random
import uuid

from .genesisuser import GenesisUser;
from .genesismcs import MCS;
from .genesisflight import Flight;
from .genesisflightplanner import plan_from_home

flights = [];

class GAPI:

    def __init__(self, server, username, password, secure=True, clientId=None, mcsId=None):
        self.secure = secure;
        self.server = server;

        self.user = GenesisUser(serverurl=self.baseURL(), username=username, password=password);
        self.mcs = MCS(serverURL=self.baseURL(), user=self.user, clientId=clientId, mcsId=mcsId);

    def unauthenticate(self):
        return self.user.unauthenticate()

    def baseURL(self):
        protocol = {True: 'https', False: 'http'}[self.secure];
        return f'{protocol}://{self.server}';

    def username(self):
        return self.user.username()

    def flights(self):
        return list(map(lambda f: f.flightId(), flights))

    def startFlight(self, home=None, plan=None):
        random_home = {
            "latitude": 12.97672 + random.uniform(0.01, 0.09),
            "longitude": 77.64654 + random.uniform(0.01, 0.09)
        }
        home = home if home else random_home
        plan = plan if plan else plan_from_home(home)
        mcs = MCS(serverURL=self.baseURL(), user=self.user, clientId=self.mcs.clientId(), mcsId=f'{self.mcs.mcsId()}-{str(uuid.uuid4())[:8]}');
        flight = Flight(server=self.baseURL(), mcs=mcs, user=self.user, home=home);
        flight.register(plan)
        flight.start()
        flights.append(flight)
        return flight.flightId()

    def removeFlight(self, flightId=None):
        flight = flights.pop()
        flight.stop()
        return flight.flightId()