import asyncio
import websockets

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://localhost:8002/')

    name = input("What's your name? ")
    yield from websocket.send(name)
    print("> {}".format(name))

    greeting = yield from websocket.recv()
    print("< {}".format(greeting))

    yield from websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
