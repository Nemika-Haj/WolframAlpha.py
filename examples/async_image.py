import wolfram, asyncio

app = wolfram.AsyncApp("APP_ID")

async def getQuery():
    data = await app.simple("Population of America")

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(getQuery())
finally:
    loop.close()