# **WolframAlpha Python API Wrapper**
This is an API wrapper for the [Wolfram Alpha API](https://www.wolframalpha.com/). It contains functions for the `Simple`, `Short Answers`, `Full Results` and `Conversational` APIs.

## Installation
**Python 3.5 of higher is required**

**Linux & macOS**
```
python3 -m pip install wolfram.py
```

**Windows**
```
py -3 -m pip install wolfram.py
```

You can always use the Github Dev version before the release on Pypi by cloning the repo and upgrading the package locally.

## Getting Started
- You must have a **WolframAlpha** account in order to get the **AppID**. You can create an account [here](https://account.wolfram.com/login/oauth2/sign-in).
- Then you must create an application at the [WolframAlpha Developer Portal](https://developer.wolframalpha.com/portal/myapps/index.html).
![AppID](https://i.imgur.com/VauZobK.png)
- Copy the AppID. You will use this to initialize the **WolframPy Application** later on.

## Application Example
```py
from wolfram import App

wolfram = App("APP_ID") # Make sure to replace the ID with your own


"""
This will generate an image with information about the american population and save it with the name "america_population.png". If no second param is provided, it will be saved as "wolframpy_content.png"
"""
wolfram.simple("Population of America", "america_population")
```


# Documentation
> `class wolfram.App(appID)`
```py
class App:
    def __init__(self, appID):
        self.id = appID
        self.SIMPLE_BASE = "https://api.wolframalpha.com/v1/simple"
        self.FULL_BASE = "https://api.wolframalpha.com/v2/query"
        self.SHORT_BASE = "http://api.wolframalpha.com/v1/result"
        self.CONV_BASE = "http://api.wolframalpha.com/v1/conversation.jsp"

    """
    Create a request to the WolframAPI
    """
    def create_request(self, BASE, **kwargs):
        return requests.get(BASE + "?" + '&'.join(f"{i}={kwargs[i]}" for i in kwargs) + "&appid=" + self.id)

    """
    Fetch an info image and save it locally

    Example: wolfram.App(app_id).simple("Value of Gold", "valueOfGold")
    """
    def simple(self, query:lambda arg:fix_format(arg), fp:lambda arg:str(arg)="wolframpy_content"):
        _data = self.create_request(self.SIMPLE_BASE, i=query)

        if _data.status_code == 200:
            with open(fp+".png", "wb") as f:
                for chunk in _data.iter_content(1024):
                    f.write(chunk)
        
        if _data.status_code == 404:
            raise APIError("The WolframAPI is currently unreachable!")
        
        if _data.status_code == 501:
            raise InputError("Could not understand input.")

    """
    Receive a dictionary of information about the query. Recommended for experts.

    Example: wolfram.App(app_id).full("Value of Gold")
    """
    def full(self, query:lambda arg:fix_format(arg)):
        return self.create_request(self.FULL_BASE, input=query, output="json").json()

    """
    Receive a line-long answer to a query
    """
    def short(self, query:lambda arg:fix_format(arg)):
        return self.create_request(self.SHORT_BASE, i=query).text

    """
    Use the ConversationalAPI to talk. Returns a dictionary

    Example: wolfram.App(app_id).talk("How are you?")
    """
    def talk(self, query:lambda arg:fix_format(arg)):
        return self.create_request(self.CONV_BASE, i=query, s=5).json()
```

## Asynchronous Usage
### Example
```py
import wolfram, asyncio, json

app = wolfram.AsyncApp("APP_ID")

async def getQuery():
    data = json.loads(await app.full("Population of America"))
    print(data)
    with open("wolfram.json", "w+") as f:
        json.dump(data, f, indent=4)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(getQuery())
finally:
    loop.close()
```
**(!)** The `SimpleAPI` is not supported in `async` yet! 