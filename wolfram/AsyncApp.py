import aiohttp, asyncio, requests, json

from .errors import *

def fix_format(string):
    keys = {
        " ": "+",
        "/": "\/",
        "'": "\'",
        '"': '\"'
    }

    for key in keys:
        string.replace(key, keys[key])
    return string

class AsyncApp:
    def __init__(self, appID):
        self.id = appID
        self.SIMPLE_BASE = "https://api.wolframalpha.com/v1/simple"
        self.FULL_BASE = "https://api.wolframalpha.com/v2/query"
        self.SHORT_BASE = "http://api.wolframalpha.com/v1/result"
        self.CONV_BASE = "http://api.wolframalpha.com/v1/conversation.jsp"

    async def create_request(self, BASE, **kwargs):
        url = BASE + "?" + '&'.join(f"{i}={kwargs[i]}" for i in kwargs) + "&appid=" + self.id

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                return json.loads(await request.text())

    async def full(self, query:lambda arg:fix_format(arg)):
        _data = await self.create_request(self.FULL_BASE, input=fix_format(query), output="json")
        return _data

    async def short(self, query:lambda arg:fix_format(arg)):
        return await (await self.create_request(self.SHORT_BASE, i=query)).text()

    async def talk(self, query:lambda arg:fix_format(arg)):
        return (await self.create_request(self.CONV_BASE, i=query, s=5)).json()