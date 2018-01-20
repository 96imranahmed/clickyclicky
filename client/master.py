from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pymouse import PyMouse
import time

from pynput import mouse, keyboard


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
    ws = create_connection("ws://35.178.5.103:9000")
    # ws = create_connection("ws://127.0.0.1:9000")
    ws.settimeout(0.05)
    send_blocking(ws, connect_message)
    return ws

def no_longer_active():
    """wtf?"""
    # MOVE the cursor to the new position
    # block master mouse presses
    pass

def now_active():
    # MOVE cursor to 10 x-pixels from the right
    # unblock master mouse presses
    pass

def master():
    master_active = True
    # GET SCREEN DIM
    m = PyMouse()
    xdim, ydim = m.screen_size()
    ws = create_socket('s0:0:%d,%d' % (xdim, ydim))

    while True:
        m_con = mouse.Controller()
        k_con = keyboard.Controller()
        # print("INPUT TIME")
        # a = input()
        # send_non_blocking(ws,a)

        # check position
        x, y = m_con.position

        if master_active:

            # if within screen, continue
            if not x > xdim - 5:
                continue
            # if not, send u message to server
            else:
                monosodium_glutamate =  'u1:%d,%d' % (10, y)
                # wait for a response
                send_blocking(ws, monosodium_glutamate)

                # CHANGE MASTER ACTIVE TO FALSE
                master_active = False

                # MOVE the cursor to the new position
                # block master mouse presses
                no_longer_active()

        else:
            if not x < 5:
                # send logic
                monosodium_glutamate = get_events()
                send_non_blocking(ws, monosodium_glutamate)
            else:
                # now master is back in control
                master_active = True

                # MOVE cursor to 10 x-pixels from the right
                # unblock master mouse presses
                now_active()



if __name__ == '__main__':
    master()
