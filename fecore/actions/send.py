"""
SEND has two channels of course, lconn for long connection and sconn for short one.
"""
import asyncio

from fecore.utils import *


SEND_LCONN = 'lconn'
SEND_SCONN = 'sconn'

ws_url = 'wss://maicadev.monika.love/websocket'
http_url = 'https://maicadev.monika.love/api'

servers_list = {}

async def send(connection, *args):
    """
    SEND sconn /savefile post `{"mas_playername": ...}`
    """
    channel, carriage = args
    match channel:
        case SEND_SCONN:
            result_json = await async_webrequest(http_url + carriage[0], *carriage[1:])

            # Here we must list all possible sconn endpoints and their actions
