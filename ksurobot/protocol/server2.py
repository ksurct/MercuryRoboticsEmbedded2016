import websockets
from asyncio import Queue
import asyncio


class RepeatedTask(object):
    def __init__(self, time, cmd):
        self.running = False
        self.time = time
        self.cmd = cmd
        self.current_task = None

    async def tick(self):
        self.cmd()

    async def runtime(self):
        while True:
            await asyncio.sleep(self.time)
            if not self.running:
                return
            await self.tick()

    async def start(self):
        self.running = True
        asyncio.ensure_future(self.runtime())

    async def stop(self):
        self.running = False


class ClientlessWebSocketServer(object):
    def __init__(self, port):
        self._active_connections = set()
        self.port = port
        self.server = None
        self.queue = Queue()

    async def start_server(self):
        self.server = await websockets.serve(self.handle_new_connection, '0.0.0.0', self.port)

    async def stop_server(self):
        await self.server.close()
        await self.server.wait_closed()
        self.server = None

    async def handle_new_connection(self, ws, path):
        logger.info("WS connection open")
        self._active_connections.add(ws)
        while True:
            result = await ws.recv()
            if result is None:
                logger.info("WS connection close")
                self._active_connections.remove(ws)
                return
            await self.handle_msg(result)

    async def handle_msg(self, msg):
        await self.queue.put(msg)

    async def recv(self):
        return await self.queue.get()

    async def send(self, msg):
        await asyncio.wait([ws.send(msg) for ws in self._active_connections])
