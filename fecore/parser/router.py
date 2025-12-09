import asyncio
import re

from typing import *
from fecore.utils import *
from fecore.actions import *

DEMAND = 'DEMAND'
CONFIRM = 'CONFIRM'

prefix_set = {DEMAND, CONFIRM}

SYNC = 'SYNC'
SEND = 'SEND'
PERFORM = 'PERFORM'
SET = 'SET'
STATE = 'STATE'

action_set = {SYNC, SEND, PERFORM, SET, STATE}

UNDEFINED = 'UNDEFINED'

re_quote = re.compile(r'[^\\](`)|^(`)', re.S)
re_escaped_quote = re.compile(r'\\`')

class Command():
    """I'm not exactly sure..."""

    demand: bool = False
    type = UNDEFINED
    channel = UNDEFINED
    params = []

    # -1 for inf
    _waiting_channel = 0
    _waiting_param = 0

    def __init__(self, protocol):
        self.protocol = protocol

    def _handle_prefix(self, stat):
        if stat == DEMAND:
            self.demand = True
        elif stat == CONFIRM:
            self.type = CONFIRM

    def _handle_action(self, stat):
        """
        Up to now, all actions should have a channel following.
        Params are to be captured and passed through.
        """
        self._waiting_channel = 1
        self._waiting_param = -1
        self.type = stat

    def add_stat(self, stat):
        if self._waiting_channel != 0:
            self.channel = stat
            if self._waiting_channel > 0:
                self._waiting_channel -= 1
        elif self._waiting_param != 0:
            self.params.append(stat)
            if self._waiting_param > 0:
                self._waiting_param -= 1

        elif stat in prefix_set:
            self._handle_prefix(stat)
        elif stat in action_set:
            self._handle_action(stat)

    async def dispatch(self):
        ...

def cmd_split(message: str):
    """This splits a command into statements."""
    stats = []
    while message:
        message = message.strip()

        if message[0] == '`':
            message = message[1:]
            next_quote = re_quote.search(message)
            stats.append(message[:next_quote.end() - 1])
            message = message[next_quote.end():]

        else:
            if ' ' in message:
                stats.append(message[:message.index(' ')])
                message = message[message.index(' ') + 1:]
            else:
                stats.append(message)
                message = ''
    
    for i in range(len(stats)):
        stats[i] = re_escaped_quote.sub('`', stats[i])

    return stats

async def router(protocol, stats: list):
    """This routes a list of statements into procedures."""
    command = Command(protocol)
    for stat in stats:
        command.add_stat(stat)
    await command.dispatch()

if __name__ == "__main__":
    stats = cmd_split(r'PERFORM log `info` `MFocus tool chain round 1 ...` `` `1\``')
    print(stats)