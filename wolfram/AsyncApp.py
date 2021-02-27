import aiohttp, asyncio, requests, json, aiofiles

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

class AsyncApp:
    def __init__(self, appID):
        self.id = appID
        self.SIMPLE_BASE = "https://api.wolframalpha.com/v1/simple"
        self.FULL_BASE = "https://api.wolframalpha.com/v2/query"
        self.SHORT_BASE = "http://api.wolframalpha.com/v1/result"
        self.CONV_BASE = "http://api.wolframalpha.com/v1/conversation.jsp"

    async def create_request(self, BASE, **kwargs):
        url = BASE + "?" + '&'.join(f"{i}={fix_format(kwargs[i])}" for i in kwargs) + "&appid=" + self.id

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                return await request.text()
    
    async def create_simple_request(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            url = self.SIMPLE_BASE + "?" + '&'.join(f"{i}={fix_format(kwargs[i])}" for i in kwargs) + "&appid=" + self.id
            async with session.get(url) as request:
                return await request.read()

    async def simple(self, query:str, fp:str="wolfram_content"):
        query = fix_format(query)
        _data = await self.create_simple_request(i=query)

        f = await aiofiles.open(f'{fp}.png', mode='wb+')
        await f.write(_data)
        await f.close()

    async def full(self, query:str):
        query = fix_format(query)
        _data = await self.create_request(self.FULL_BASE, input=fix_format(query), output="json")
        return json.loads(_data)

    async def short(self, query:str):
        query = fix_format(query)
        return await self.create_request(self.SHORT_BASE, i=query)

    async def talk(self, query:str):
        query = fix_format(query)
        _data = await self.create_request(self.CONV_BASE, i=query, s=5)
        return json.loads(_data)