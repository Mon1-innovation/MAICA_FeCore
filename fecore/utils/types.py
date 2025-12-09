DEMAND = 'DEMAND'
CONFIRM = 'CONFIRM'

prefix_set = {DEMAND, CONFIRM}

SYNC = 'SYNC'
SEND = 'SEND'
SHOW = 'SHOW'
SET = 'SET'
STATE = 'STATE'

action_set = {SYNC, SEND, SHOW, SET, STATE}

UNDEFINED = 'UNDEFINED'

SEND_SCONN = 'sconn'
SEND_LCONN = 'lconn'

send_channels = {SEND_SCONN, SEND_LCONN}

SHOW_LOG1 = 'log1'
SHOW_LOG2 = 'log2'
SHOW_LOG3 = 'log3'
SHOW_SCREEN = 'screen'
SHOW_DIALOG = 'dialog'

show_channels = {SHOW_LOG1, SHOW_LOG2, SHOW_LOG3, SHOW_SCREEN, SHOW_DIALOG}

STATE_MAINSTAT = 'mainstat'

state_channels = {STATE_MAINSTAT}