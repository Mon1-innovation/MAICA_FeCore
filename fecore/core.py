"""
First priorities:

- One fecore should only serve one feui, so kick stale connections


"""

import asyncio

from typing import *

_server = None

async def handle_message(message):
    ...




class CoreUIProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        global _server
        if _server:
            _server.transport.close()
        _server = self

        peername = transport.get_extra_info('peername')
        print(f'Connection from {peername}')
        self.transport = transport
        self.buffer = bytearray()

    def data_received(self, data):
        self.buffer.extend(data)

        while True:
            newline_index = self.buffer.find(b'\n')
            if newline_index != -1:
                message = self.buffer[:newline_index].decode('utf-8')
                print(f"Received message: {message}")

                loop = asyncio.get_running_loop()
                task = loop.create_task(handle_message(message))

                del self.buffer[:newline_index + 1]
            else:
                break

    def send_data(self, data):
        self.transport.write(data + b'\n')

    def connection_lost(self, exc):
        return self.transport.close()

_server: Optional[CoreUIProtocol]

async def main():
    host = '127.0.0.1'
    port = 8888
    
    try:
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            CoreUIProtocol,
            host,
            port,
        )
        
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f"MAICA Fe core started, listening on {addrs}")
        
        async with server:
            await server.serve_forever()
            
    except OSError as e:
        print(f"Server start failed: {e}")

    except KeyboardInterrupt:
        print("\nMAICA Fe core shutting down...")

if __name__ == "__main__":
    asyncio.run(main())
