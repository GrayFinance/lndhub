import requests

class LndHub:

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.__token = dict()
        self.__username = username
        self.__password = password

    def call(self, method: str, path: str, params=None, json=None):
        if not (self.__token):
            self.get_auth()

        r = requests.request(
            method=method, 
            url=self.url + path, 
            json=json,
            params=params, 
            headers={"Authorization": "Bearer " + self.__token["access_token"]}
        )
        return r.json()

    def get_auth(self) -> dict:
        data = {"login": self.__username, "password": self.__password}
        self.__token = requests.post(f"{self.url}/auth?type=auth", json=data).json()

    def payinvoice(self, invoice: str) -> dict:
        data = {"invoice": invoice}
        return self.call("POST", "/payinvoice", json=data)

    def get_balance(self):
        return self.call("GET", "/balance")

    def get_transactions(self, limit=10, offset=0):
        data = {"limit": limit, "offset": offset}
        return self.call("GET", "/gettxs", json=data)

    def addinvoice(self, value: int, memo=""):
        data = {"amt": value, "memo": memo}
        return self.call("POST", "/addinvoice", json=data)

    def check_payment(self, payment_hash: str) -> dict:
        return self.call("GET", f"/checkpayment/{payment_hash}")
