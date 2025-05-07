import websockets
import asyncio


class RPAWebSocket:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create it
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_data, rpa_tracker):
        self.data = config_data
        self.rpa_tracker = rpa_tracker
        self.client = None
        self.loop = asyncio.get_event_loop()

    async def connect_to_socket_server(self):
        self.client = await websockets.connect(uri=self.data["socket_host"])

    async def send_message(self, message):
        if self.client:
            await self.client.send(message)
    
    async def receive_message(self):
        while True:
            if self.client:
                response = await self.client.recv()
                print(f"Received: {response}")  
    
    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
