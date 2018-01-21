from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import time
import ctypes

SLAVE_ID = 1

ws = None
m_con = mouse.Controller()
k_con = keyboard.Controller()
BUTTON_LIST = [Button.left, Button.middle, Button.right]

def process_message(msg):
    global m_con, k_con
    msg_type = msg[0]
    msg = msg[1:]
    if msg_type == 'm':
        # Process coordinates
        coords = [int(i) for i in msg.split(',')]
        m_con.position = coords
    elif msg_type == 'c':
        # Process button
        cmd_split = msg.split(':')
        c_btn = BUTTON_LIST[int(cmd_split[0])]
        is_press = bool(int(cmd_split[1]))
        coords = [int(i) for i in cmd_split[2].split(',')]
        m_con.position = coords
        if is_press:
            print("clicky clicky")
            m_con.press(c_btn)
        else:
            m_con.release(c_btn)
    elif msg_type == 'l':
        # Process scroll
        dx, dy = [int(i) for i in msg.split(':')]
        m_con.scroll(dx, dy)
    elif msg_type == 'i':
        return NotImplementedError


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
            dead = False
        except:
            pass

def create_socket(connect_message):
    ws = create_connection("ws://35.178.5.103:9000")
    # ws = create_connection("ws://127.0.0.1:9000")
    ws.settimeout(0.05)
    send_blocking(ws, connect_message)
    return ws


def slave():
    global ws
    # GET SCREEN DIM
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    xdim, ydim = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    ws = create_socket('s%d:1:%d,%d' % (SLAVE_ID, xdim, ydim))

    while True:
        no_msg = True
        while no_msg:
            try:
                current_msg = ws.recv()
                no_msg = False
                process_message(current_msg)
            except:
                pass
    

if __name__ == '__main__':
    slave()
