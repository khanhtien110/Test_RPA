import websockets
import asyncio
import json
class RPAWebSocket:
    def __init__(self, config_data, rpa_tracker, handle_message):
        self.data = config_data
        self.rpa_tracker = rpa_tracker
        self.websocket = None
        self.handle_message = handle_message
        self.is_connected = False
    
    async def open_connect(self):
        while True:
            if self.is_connected:  # Nếu đã kết nối, không cần kết nối lại
                    await asyncio.sleep(5)
                    continue
            try:
                print("🔄 Đang kết nối lại...")
                self.websocket = await websockets.connect(self.data["connectString"], ping_interval=None)
                print("✅ WebSocket đã kết nối.")
                self.is_connected = True
                # Chạy các tác vụ song song
                asyncio.create_task(self.check_connection())  # Kiểm tra ping/pong
                asyncio.create_task(self.listen_for_messages())  # Nhận tin nhắn
                
            except Exception as e:
                print(f"⚠️ Lỗi kết nối: {e}, thử lại sau 5s...")
                await asyncio.sleep(5)  # Chờ 5 giây trước khi thử kết nối lại
            
    async def send_message(self, message):
        try:
            if message and self.websocket:
                await self.websocket.send(message=message)
                response = await self.websocket.recv()
                self.rpa_tracker.info(f"Received: {response}")
            else:
                 self.rpa_tracker.error(f"Can not send message: {message}")
        except Exception as e:
            self.rpa_tracker.error(f"Can not send message: {message}")
            print(e)
    
    async def listen_for_messages(self):
        """Continuously listens for messages from the server."""
        if not self.websocket:
            print("❌ WebSocket is not connected. Cannot listen for messages.")
            return
        try:
            async for message in self.websocket:
                asyncio.create_task(self.handle_message(message))
        except websockets.exceptions.ConnectionClosed:
            print("🔴 WebSocket connection closed.")
        except Exception as e:
            print(f"❌ Error receiving message: {e}")
    
    async def check_connection(self):
        """Check WebSocket connection status every 5 seconds."""
        while True:
            await asyncio.sleep(5)
            if self.websocket:
                try:
                    pong  = await self.websocket.ping()
                    await asyncio.wait_for(pong, timeout=3)  # Wait for pong response (max 3 sec)
                    print("✅ WebSocket is active (pong received).")
                except Exception as e:
                    self.is_connected = False
                    print("⚠️ No pong response, reconnecting...")
                    await self.close_connect()
                    break
    
    async def reconnect(self):
        """Reconnect to the WebSocket server."""
        await self.close_connect()
        await asyncio.sleep(2)  # Wait before reconnecting
        print("🔄 Reconnecting to WebSocket...")
        await self.open_connect()
    
    async def close_connect(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None
            