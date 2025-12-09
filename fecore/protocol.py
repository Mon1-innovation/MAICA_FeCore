"""
Here we clarify the message structure, perhaps call it ActionQL.

According to my designs, it looks pretty much like SQL queries, but we define our own statements.  
We call them 'Commands', since they're action based.   
Commands are full-duplex, but possible actions differ a little between peers, of course.  
We take UI -> Core as example:

| Statement | I want you to... |
| --------- | ---------------- |
| SYNC | Get / push a status to keep sync |
| SEND | Send the corresponding data to remote, and send me command back |
| PERFORM | Do something in a specific channel |
| SET | Set a variable or what |
| STATE | Enter or leave a state in a specific channel |

...

An action statement takes one necessary 'channel', followed by none or several 'parameters'.
Statements are separated by spaces, so statement with spaces inside should be wrapped by ``s.
> To passthrough `s, escape them.

As examples:

- [UI -> Core] SYNC status_code
- [Core -> UI] SET status_code `10302`
-----
- [UI -> Core] SEND default_settings
- [Core -> UI] SET default_settings `{"enable_mfocus": true, ...}`
-----
- [UI -> Core] SEND chat_query `你好啊`
- [Core -> UI] STATE main_status chat_recv
- [Core -> UI] PERFORM log `info` `MFocus tool chain round 1 ...`
- [Core -> UI] PERFORM log_file `info` `200` `MFocus tool chain round 1 ...`
- [Core -> UI] PERFORM dialog `你好啊, [player]!{nw}` `1eua`
- [Core -> UI] PERFORM dialog `你今天过得怎么样?` `1eka`
- [Core -> UI] PERFORM dialog `想我了吗?` `1esa`
- [Core -> UI] SET status_code `10302`
- [Core -> UI] PERFORM mtrigger `alter_affection` `1.0`
- [Core -> UI] STATE main_status chat_idle

Then, we have prefixes and postfixes:
| Statement | I want you to... |
| --------- | ---------------- |
| DEMAND | Prefix. The involving command should be executed blockingly |
| CONFIRM | Prefix. Kinda reserved |

...

As examples:

- [UI -> Core] DEMAND SEND chat_login `my_token`
- [UI -> Core] SEND chat_query `你好啊`
- [Core -> UI] PERFORM log `info` `Login success ...`
- [Core -> UI] STATE main_status chat_idle
- [Core -> UI] STATE main_status chat_recv
...
-----
- [UI -> Core] DEMAND SEND chat_login `my_token2`
- [UI -> Core] SEND chat_query `你好啊`
- [Core -> UI] PERFORM log `info` `Login failed ...`
- [Core -> UI] STATE main_status login_failed
- [Core -> UI] PERFORM log `warn` `Query needs login ...`

"""

import asyncio

from typing import *
from fecore.parser.router import router

class CoreUIProtocol(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        self.lock = asyncio.Lock()

    def connection_made(self, transport):
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
                task = loop.create_task(router(self, message))

                del self.buffer[:newline_index + 1]
            else:
                break

    def send_data(self, data):
        self.transport.write(data + b'\n')

    def connection_lost(self, exc):
        return self.transport.close()