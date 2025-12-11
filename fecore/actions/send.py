"""
SEND has two channels of course, lconn for long connection and sconn for short one.
"""
import asyncio
import json

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
    channel, endpoint, type, *carriage = args
    match channel:
        case SEND_SCONN:
            content = carriage[0]
            result_json = await async_webrequest(http_url + endpoint, type, *carriage)

            # Here we must list all possible sconn endpoints and their actions
            match (endpoint, type):

                case ('/history', 'get'):
                    if result_json.get('success'):
                        with open(os.path.join(MAS_DIR, SUBMODS_DIR, MAICA_CHATSUBMOD_DIR, 'chat_history.txt')) as history_file:
                            history_file.write(json.dumps(result_json.get('content')))
                        connection.send_data('PERFORM renpy_notify `MAICA: 历史已导出至game/Submods/MAICA_ChatSubmod/chat_history.txt`')
                    else:
                        connection.send_data(f'PERFORM renpy_log error `{result_json.get('exception')}`')

                case ('/preferences', 'get'):
                    pass

                case ('/register', 'get'):
                    if result_json.get('success'):
                        vars.access_token = json.loads(result_json)
                        connection.send_data('SET access_token ' + vars.access_token)
                    else:
                        connection.send_data(f'PERFORM renpy_log error `{result_json.get('exception')}`')

                case ('/legality', 'get'):
                    verification_object = json.loads('content').get('object', 'access_token')
                    if result_json.get('success'):
                        connection.send_data('SET ')