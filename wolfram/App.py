import requests

from .errors import *

def fix_format(string):
    keys = {
        " ": "+",
        "/": "\/",
        "'": "\'",
        '"': '\"',
        "+": "%2B"
    }

    for key in keys:
        string = string.replace(key, keys[key])
    return string

class App:
    def __init__(self, appID):
        self.id = appID
        self.SIMPLE_BASE = "https://api.wolframalpha.com/v1/simple"
        self.FULL_BASE = "https://api.wolframalpha.com/v2/query"
        self.SHORT_BASE = "http://api.wolframalpha.com/v1/result"
        self.CONV_BASE = "http://api.wolframalpha.com/v1/conversation.jsp"

    def create_request(self, BASE, **kwargs):
        return requests.get(BASE + "?" + '&'.join(f"{i}={kwargs[i]}" for i in kwargs) + "&appid=" + self.id)

    def simple(self, query:str, fp:str="wolframpy_content"):
        query = fix_format(query)
        _data = self.create_request(self.SIMPLE_BASE, i=query)

        if _data.status_code == 200:
            with open(fp+".png", "wb") as f:
                for chunk in _data.iter_content(1024):
                    f.write(chunk)
        
        if _data.status_code == 404:
            raise APIError("The WolframAPI is currently unreachable!")
        
        if _data.status_code == 501:
            raise InputError("Could not understand input.")

    def full(self, query:str):
        query = fix_format(query)
        return self.create_request(self.FULL_BASE, input=query, output="json").json()

    def short(self, query:str):
        query = fix_format(query)
        return self.create_request(self.SHORT_BASE, i=query).text

    def talk(self, query:str):
        query = fix_format(query)
        return self.create_request(self.CONV_BASE, i=query, s=5).json()