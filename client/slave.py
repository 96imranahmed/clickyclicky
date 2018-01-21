from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pymouse import PyMouse
import time

ws = None
m_con = mouse.Controller()
k_con = keyboard.Controller()


def send_non_blocking(ws, message):
    # happy go lucky, "at most once" message sending
    ws.send(message)

def send_blocking(ws, message):
    # Send the message and hope for a return
    ws.send(message)
    dead = True
    while dead:
        try:
            tmp = ws.recv()
            print("not swallowing")
            print(tmp)
            dead = False
        except:
            pass

def create_socket(connect_message):
    # ws = create_connection("ws://35.178.5.103:9000")
    ws = create_connection("ws://127.0.0.1:9000")
    ws.settimeout(0.05)
    send_blocking(ws, connect_message)
    return ws


def slave():
    global ws
    # GET SCREEN DIM
    m = PyMouse()
    xdim, ydim = m.screen_size()
    ws = create_socket('s1:1:%d,%d' % (xdim, ydim))

    while True:
        print("INPUT TIME")
        a = input()
        send_non_blocking(ws,a)

if __name__ == '__main__':
    slave()
