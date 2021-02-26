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