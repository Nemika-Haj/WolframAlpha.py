import wolfram

app = wolfram.App("APP_ID")

while True:
    query = input("")

    _data = app.talk(query)
    print(_data['result'] if 'result' in _data else 'I did not understand :(')