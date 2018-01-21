from __future__ import division
from __future__ import print_function
from websocket import create_connection
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import time
import ctypes
import pyperclip

SLAVE_ID = 1

ws = None
m_con = mouse.Controller()
k_con = keyboard.Controller()
BUTTON_LIST = [Button.left, Button.middle, Button.right]

<<<<<<< HEAD

PORT = 9002
copyserver = WebsocketServer(PORT, '0.0.0.0')
copyserver_remote_object = None

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


rosetta = {}

PORT = 9002
copyserver = WebsocketServer(PORT, '0.0.0.0')
copyserver_remote_object = None

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


def process_message(msg):
    global m_con, k_con, rosetta
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
            m_con.press(c_btn)
        else:
            m_con.release(c_btn)
    elif msg_type == 'l':
        # Process scroll
        dx, dy = [int(i) for i in msg.split(':')]
        m_con.scroll(dx, dy)
    elif msg_type == 'i':
        cmd_split = msg.split(":")
        ch = cmd_split[0]
        is_press = bool(int(cmd_split[1]))
        if not len(ch) == 1:
            ch = rosetta[cmd_split[0]]
        if is_press:
            k_con.press(ch)
        else:
            k_con.release(ch)     

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

    # start the copyserver here and tell the other server to talk to us
    _thread.start_new_thread( start_copyserver, ())
    send_blocking(ws, "x%d" % SLAVE_ID)

    cur_clip = pyperclip.paste()


    while True:
        no_msg = True
        while no_msg:
            try:
                current_msg = ws.recv()
                no_msg = False

                # first, do clipboard ops
                new_clip = pyperclip.paste()
                if new_clip != cur_clip:
                    cur_clip = new_clip
                    clipmsg = "v" + cur_clip
                    send_non_blocking(ws, clipmsg)
                    process_message(current_msg)
            except:
                pass
    

if __name__ == '__main__':
    for key in keyboard.Key:
        rosetta[str(key)] = key
    slave()
