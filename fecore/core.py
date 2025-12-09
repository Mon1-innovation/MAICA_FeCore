"""
I assume we can have multiple connections to make threading/asyncio UI easier.
"""

import asyncio

from typing import *
from fecore import protocol

async def main():
    host = '127.0.0.1'
    port = 8888
    
    try:
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            protocol.CoreUIProtocol,
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
