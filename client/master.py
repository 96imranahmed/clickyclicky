from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pymouse import PyMouse
import time

import ctypes
from ctypes import windll, wintypes

import enum

from pynput import mouse, keyboard

from pynput._util import NotifierMixin
from pynput._util.win32 import (
    INPUT,
    INPUT_union,
    ListenerMixin,
    MOUSEINPUT,
    SendInput,
    SystemHook)

ws = None

m_con = mouse.Controller()
k_con = keyboard.Controller()

deadmau5 = False


WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_MOUSEMOVE = 0x0200
WM_MOUSEWHEEL = 0x020A
WM_MOUSEHWHEEL = 0x020E
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
_WHEEL_DELTA = 120

SCROLL_BUTTONS = {
    WM_MOUSEWHEEL: (0, 1),
    WM_MOUSEHWHEEL: (1, 0)}


class Button(enum.Enum):
    """The various buttons.
    """
    unknown = None
    left = (MOUSEINPUT.LEFTUP, MOUSEINPUT.LEFTDOWN)
    middle = (MOUSEINPUT.MIDDLEUP, MOUSEINPUT.MIDDLEDOWN)
    right = (MOUSEINPUT.RIGHTUP, MOUSEINPUT.RIGHTDOWN)


CLICK_BUTTONS = {
    WM_LBUTTONDOWN: (Button.left, True),
    WM_LBUTTONUP: (Button.left, False),
    WM_MBUTTONDOWN: (Button.middle, True),
    WM_MBUTTONUP: (Button.middle, False),
    WM_RBUTTONDOWN: (Button.right, True),
    WM_RBUTTONUP: (Button.right, False)}

def on_move(x, y):
    # print('Pointer moved to {0}'.format(
    #     (x, y)))
    pass

def on_click(x, y, button, pressed):
    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y)))
    # if not pressed:
    #     # Stop listener
    #     return False
    pass

def on_scroll(x, y, dx, dy):
    pass

def block_maus_callback(msg, data):
    global l, deadmau5
    global ws

    if deadmau5:
        x_pos = data.pt.x
        y_pos = data.pt.y

        if msg in CLICK_BUTTONS:
            button, pressed = CLICK_BUTTONS[msg]
            flag = not pressed
            monosodium_glutamate = "i1:"
            l.suppress_event()
            

        elif msg in SCROLL_BUTTONS:

            dd = wintypes.SHORT(data.mouseData >> 16).value // _WHEEL_DELTA
            mx, my = SCROLL_BUTTONS[msg]
            dx = dd * mx
            dy = dd * my

            l.suppress_event()

        elif msg == WM_MOUSEMOVE:
            # master is dead; 1 < 2
    return True


l = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll,
        win32_event_filter = block_maus_callback)



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

def no_longer_active(x, y):
    global deadmau5
    # MOVE the cursor to the new position
    m_con.position = (10, y)

    # block master mouse presses
    deadmau5 = True


def now_active(xdim, y):
    # MOVE cursor to 10 x-pixels from the right
    # unblock master mouse presses
    m_con.position = (10, y)
    
    deadmau5 = False

def master():
    global ws
    master_active = True
    # GET SCREEN DIM
    m = PyMouse()
    xdim, ydim = m.screen_size()
    ws = create_socket('s0:0:%d,%d' % (xdim, ydim))

    while True:
        # print("INPUT TIME")
        # a = input()
        # send_non_blocking(ws,a)

        global m_con, k_con

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
                no_longer_active(x,y)

        else:
            if not x < 5:
                # send logic
                pass
                # monosodium_glutamate = get_events()
                # send_non_blocking(ws, monosodium_glutamate)
            else:
                # now master is back in control
                master_active = True

                # MOVE cursor to 10 x-pixels from the right
                # unblock master mouse presses
                now_active(xdim, y)



if __name__ == '__main__':
    global l
    l.start()
    l.join()
    master()
