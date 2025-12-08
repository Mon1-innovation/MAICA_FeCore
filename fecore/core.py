"""
First priorities:

- One fecore should only serve one feui, so kick stale connections


"""

import asyncio

from typing import *

_server = None

async def handle_message(message):
    ...

async def message_router(message):
    """
    Here we clarify the message structure.

    According to my designs, it looks pretty much like SQL queries, but we define our own statements.  
    We call them 'Commands', since they're action based.   
    Commands are full-duplex, but possible actions differ a little, of course.  
    We take UI -> Core as example:

    | Statement | I want you to... |
    | --------- | ---------------- |
    | GET | Send me the corresponding command |
    | SEND | Send the corresponding data to remote, and send me command back |
    | SHOW | Display something in a specific channel, perhaps we should call it 'DO' |
    | SET | Set a variable or what |
    | STATE | Enter or leave a state in a specific channel |

    ...

    As examples:
    
    - [UI -> Core] GET status_code
    - [Core -> UI] SET status_code `10302`
    -----
    - [UI -> Core] SEND default_settings
    - [Core -> UI] SET default_settings `{"enable_mfocus": true, ...}`
    -----
    - [UI -> Core] SEND chat_query `你好啊`
    - [Core -> UI] STATE main_status chat_recv
    - [Core -> UI] SHOW log `info` `MFocus tool chain round 1 ...`
    - [Core -> UI] SHOW log_file `info` `200` `MFocus tool chain round 1 ...`
    - [Core -> UI] SHOW dialog `你好啊, [player]!{nw}` `1eua`
    - [Core -> UI] SHOW dialog `你今天过得怎么样?` `1eka`
    - [Core -> UI] SHOW dialog `想我了吗?` `1esa`
    - [Core -> UI] SET status_code `10302`
    - [Core -> UI] SHOW mtrigger `alter_affection` `1.0`
    - [Core -> UI] STATE main_status chat_idle

    Then, we have prefixes and postfixes:
    | Statement | I want you to... |
    | --------- | ---------------- |
    | DEMAND | Prefix. The involving command should be executed blockingly |
    | CONFIRM | Prefix. DEMAND commands must be confirmed before executing |

    ...

    As examples:

    - [UI -> Core] DEMAND SEND chat_login `my_token`
    - [Core -> UI] CONFIRM
    - [UI -> Core] SEND chat_query `你好啊`
    - [Core -> UI] SHOW log `info` `Login success ...`
    - [Core -> UI] STATE main_status chat_idle
    - [Core -> UI] STATE main_status chat_recv
    ...
    -----
    - [UI -> Core] DEMAND SEND chat_login `my_token2`
    - [Core -> UI] CONFIRM
    - [UI -> Core] SEND chat_query `你好啊`
    - [Core -> UI] SHOW log `info` `Login failed ...`
    - [Core -> UI] STATE main_status login_failed
    - [Core -> UI] SHOW log `warn` `Query needs login ...`

    """


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
