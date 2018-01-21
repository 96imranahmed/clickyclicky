from __future__ import division
from __future__ import print_function
from websocket import create_connection
import time

import _thread

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

import pynput.keyboard._win32 as w32

import pyperclip

LST = w32.Listener(None, None)

kl = None
l = None
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
_WHEEL_DELTA = 1

SCROLL_BUTTONS = {
    WM_MOUSEWHEEL: (0, 1),
    WM_MOUSEHWHEEL: (1, 0)}


CLICK_BUTTONS = {
    WM_LBUTTONDOWN: (0, True),
    WM_LBUTTONUP: (0, False),
    WM_MBUTTONDOWN: (1, True),
    WM_MBUTTONUP: (1, False),
    WM_RBUTTONDOWN: (2, True),
    WM_RBUTTONUP: (2, False)}


PORT = 9001
copyserver = WebsocketServer(PORT, '0.0.0.0')
copyserver_remote_object = None


def on_press(key):
    pass

def on_release(key):
    pass


def preprocess_keys(msg, data):
    global kl, LST, ws
    if deadmau5:
        is_packet = data.vkCode == LST._VK_PACKET
        if is_packet:
            tup = (msg | LST._UTF16_FLAG, data.scanCode)
        else:
            tup = (msg, data.vkCode)
        key_send = LST._event_to_key(tup[0], tup[1])
        # TODO add sending logic
        kl.suppress_event()
    return True


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
            monosodium_glutamate = "c%d:%d:%d,%d" % (button, int(pressed), x_pos, y_pos)
            send_non_blocking(ws, monosodium_glutamate)
            l.suppress_event()
            
        elif msg in SCROLL_BUTTONS:
            dd = wintypes.SHORT(data.mouseData >> 16).value // _WHEEL_DELTA
            mx, my = SCROLL_BUTTONS[msg]
            dx = dd * mx
            dy = dd * my

            monosodium_glutamate = "l%d:%d" % (dx, dy)
            send_non_blocking(ws, monosodium_glutamate)
            l.suppress_event()

        elif msg == WM_MOUSEMOVE:
            monosodium_glutamate = "m%d,%d" % (x_pos, y_pos)
            send_non_blocking(ws, monosodium_glutamate)
            # master is dead; 1 < 2
    return True

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


def client_left(client, copyserver):
    pass

def new_client(client, copyserver):
    pass

def proc_copyserver_msg(client, copyserver, msg):
    global copyserver_remote_object

    if len(msg) == 0: 
        return

    if msg == 'hello':
        copyserver_remote_object = client
        copyserver.send_message(client, "k")

    elif msg.split(':')[0] == 'pyperclip':
        pyperclip.copy(msg.split(':')[1])


def start_copyserver():
    copyserver.set_fn_new_client(new_client)
    copyserver.set_fn_client_left(client_left)
    copyserver.set_fn_message_received(proc_copyserver_msg)
    copyserver.run_forever()


def create_socket(connect_message):
    # ws = create_connection("ws://35.178.5.103:9000")
    ws = create_connection("ws://127.0.0.1:9000")

    ws.settimeout(0.05)
    send_blocking(ws, connect_message)
    return ws

def no_longer_active(xdim, y, new_screen_id):
    global deadmau5
    print("no longer active")
    # MOVE the cursor to the new position
    if new_screen_id == 1:
        m_con.position = (10, y)
    elif new_screen_id == 2:
        m_con.position = (xdim-10, y)

    # block master mouse presses
    deadmau5 = True


def now_active(xdim, y, old_screen_id):
    global deadmau5
    # MOVE cursor to 10 x-pixels from the right
    # unblock master mouse presses
    if old_screen_id == 1:
        m_con.position = (xdim - 10, y)
    elif old_screen_id == 2:
        m_con.position = (10, y)
    
    deadmau5 = False

def master():
    global ws, deadmau5
    deadmau5 = False
    # GET SCREEN DIM
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    xdim, ydim = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    ws = create_socket('s0:0:%d,%d' % (xdim, ydim))

    active_screen = 0

    # start the copyserver here and tell the other server to talk to us
    _thread.start_new_thread( start_copyserver, ())
    send_blocking(ws, "x0")

    cur_clip = pyperclip.paste()


    while True:
        # print("INPUT TIME")
        # a = input()
        # send_non_blocking(ws,a)

        global m_con, k_con

        # check position
        x, y = m_con.position

        if not deadmau5:
            # first, do clipboard ops
            new_clip = pyperclip.paste()
            if new_clip != cur_clip:
                cur_clip = new_clip
                clipmsg = "v" + cur_clip
                send_non_blocking(ws, clipmsg)

            # if within screen, continue
            if  x > 5 and x < xdim - 5:
                continue
            # if in right screen : screen id 1
            elif x > xdim - 5:
                monosodium_glutamate =  'u1:%d,%d' % (10, y)
                # wait for a response
                send_blocking(ws, monosodium_glutamate)

                # MOVE the cursor to the new position
                # block master mouse presses
                no_longer_active(xdim, y, 1)
                active_screen = 1
            # if in left screen: screen id 2
            elif x < 5:
                monosodium_glutamate =  'u2:%d,%d' % (xdim-10, y)
                # wait for a response
                send_blocking(ws, monosodium_glutamate)

                # MOVE the cursor to the new position
                # block master mouse presses
                no_longer_active(xdim, y, 2)
                active_screen = 2

        else:
            if x < 5 and active_screen == 1: # GG
                # send logic
                monosodium_glutamate =  'u0:%d,%d' % (0, 0)
                # wait for a response
                send_blocking(ws, monosodium_glutamate)
                now_active(xdim, y, 1)
            elif x > xdim - 5 and active_screen == 2:
                monosodium_glutamate =  'u0:%d,%d' % (0, 0)
                # wait for a response
                send_blocking(ws, monosodium_glutamate)
                now_active(xdim, y, 2)
            else:
                pass




if __name__ == '__main__':

    kl = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        win32_event_filter = preprocess_keys
        )

    l = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll,
        win32_event_filter = block_maus_callback)


    l.start()

    print("oh boi")

    kl.start()

    print("WHOAH boi")

    master()

    l.join()
    kl.join()
