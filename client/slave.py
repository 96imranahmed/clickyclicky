from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pymouse import PyMouse
import time


def send_message_sync(ws, message, id_in):
    ws.send(message)
    result = None
    count = 0
    while result is None:
        try:
            ws.send('r'+id_in)
            result =  ws.recv()
            if result == 'k':
                result = None
        except:
            count+=1
    receipt = None
    while receipt is None:
        try:
            ws.send('k'+id_in)
            receipt =  ws.recv()
        except:
            pass
    return result

def all_synced():
    global agents
    for item in agents:
        if item == 0:
            return False
    return True

def create_socket(connect_message):
    # ws = create_connection("ws://35.178.5.103:9000")
    ws = create_connection("ws://127.0.0.1:9000")
    ws.settimeout(0.05)
    ws.send(connect_message)
    try:
        _ = ws.recv()
    except:
        pass
    return ws



def master():
    # GET SCREEN DIM
    m = PyMouse()
    xdim, ydim = m.screen_size()
    ws = create_socket('s0:0:%d,%d' % (xdim, ydim))

    while True:
        print("Enter value")
        a = input()
        ws.send(a)

if __name__ == '__main__':
    master()
