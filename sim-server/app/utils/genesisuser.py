import requests;

from threading import Timer

class GenesisUser:

    def __init__(self, serverurl, username, password):
        self.__auth_refresh_timer = None
        self._serverurl = serverurl
        self._username = username
        self.password = password
        self.authToken = ''
        
        self.authenticate()

    def authenticate(self):
        url = f'{self._serverurl}/auth/login'
        data = {
            'username': self._username,
            'password': self.password
        }
        res = requests.post(url=url, data=data)
        self.authToken = res.json()['data']['authToken']
        tokenTTL = int(res.json()['data']['tokenTTL']) - 30
        
        print(f'{self._username} authenticated...')
        print(f'refreshing auth token in {tokenTTL} seconds')

        self.__auth_refresh_timer.cancel() if self.__auth_refresh_timer else None
        self.__auth_refresh_timer = Timer(tokenTTL, self.authenticate, ())
        self.__auth_refresh_timer.start()
        return self.authToken

    def unauthenticate(self):
        self.__auth_refresh_timer.cancel() if self.__auth_refresh_timer else None
        url = f'{self._serverurl}/auth/logout/{self._username}'
        data = {
            'auth_token': self.authToken
        }
        res = requests.post(url=url, data=data)
        print(f'{self._username} un-authenticated...')
        self.authToken = ""
        return self.authToken

    def username(self):
        return self._username

    def token(self):
        return self.authToken
    