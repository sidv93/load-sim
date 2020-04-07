import requests;
import json;

class MCS():
    def __init__(self, serverURL, user, clientId, mcsId):
        self.serverURL = serverURL;
        self.user = user;
        self._clientId = clientId;
        self._mcsId = mcsId;

        self.__register();

    def clientId(self):
        return self._clientId;

    def mcsId(self):
        return self._mcsId;

    def __register(self):
        baseurl = f'{self.serverURL}/api/v1.0/mcs';
    
        res = requests.get(url = f'{baseurl}/{self.clientId()}/{self.mcsId()}', params = {'auth_token': self.user.token()});
        if res.status_code == 200:
            print(f'{self.mcsId()} from {self.clientId()} is already registered');
            return;

        data = {
            'auth_token': self.user.token(),
            'client_id': self.clientId(),
            'mcs_id': self.mcsId()
        };
        res = requests.post(url= baseurl, data=data);