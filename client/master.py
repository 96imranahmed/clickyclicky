from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pymouse import PyMouse
import time

def send_message_async(ws, message):
    # happy go lucky, "at most once" message sending
    ws.send(message)

def send_message_sync(ws, message, id_in):
    # Send the message and hope for a return
    ws.send(message)
    try:
        return ws.recv()
    except:
        # swallow it
        pass

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
        a = input()
        ws.send(a)

if __name__ == '__main__':
    master()
