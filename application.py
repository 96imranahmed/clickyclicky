# -*- coding: utf-8 -*-
from __future__ import print_function

from websocket_server import WebsocketServer

PORT = 9000
server = WebsocketServer(PORT, '0.0.0.0')

clipboard = None

class Client(object):
    def __init__(self, client_obj, client_type, client_active, client_id, dims, bdry=None):
        self.obj = client_obj
        self.client_type = client_type
        self.client_active = client_active
        self.id = client_id
        self.dim_x = dims[0]
        self.dim_y = dims[1]
        self.bdry = bdry 


# keyed by ids
cur_clients = {}

active_client_id = 0

cur_copyservers = {}

def start_server():
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()


def create_copyserver_socket(connect_message, address):
    # ws = create_connection("ws://35.178.5.103:9000")
    ws = create_connection("ws://" + address)

    ws.settimeout(0.05)
    send_blocking(ws, connect_message)
    return ws


def message_received(client, server, message):
    global cur_clients, active_client_id, cur_copyservers, clipboard

    if len(message) == 0: return

    message_type = message[0]

    msg = message[1:]

    if message_type == 'e':
        #This is a debug message
        print('Debug: ', msg)

    elif message_type == 's':
        #This is a setup message - (s{id}:{master,slave}:{x,y})
        msg_lst = msg.split(':')

        if msg_lst[1] == '0':
            print("Got master connected")
            dims = [int(i) for i in msg_lst[2].split(',')]
            c_cur = Client(client, 'master', True, int(msg_lst[0]), dims)


        else:
            print("Got slave connected")
            dims = [int(i) for i in msg_lst[2].split(',')]
            c_cur = Client(client, 'slave', False, int(msg_lst[0]), dims)

        cur_clients[int(msg_lst[0])] = c_cur

        server.send_message(client, "k")


    elif message_type == 'u':
        msg_lst = msg.split(':')
        # Firstly get the new active screen
        if active_client_id in cur_clients:
            cur_clients[active_client_id].client_active = False
        active_client_id = int(msg_lst[0])

        if active_client_id in cur_clients:
            cur_clients[active_client_id].client_active = True
            if not active_client_id == 0:
                server.send_message(cur_clients[active_client_id].obj, 'm' + msg)


            # send the clipboard content to the active client
            rel_copyserver_ws = cur_copyservers[active_client_id]
            rel_copyserver_ws.send("pyperclip:" + str(clipboard))


        print("CONTEXT SWITCH TO %d" % active_client_id)

        # send message to master
        server.send_message(cur_clients[0].obj, '<3')


    elif message_type == 'm' or message_type == 'l' or message_type == 'c' or message_type == 'i' \
            or message_type == 'k':
        if active_client_id in cur_clients:
            server.send_message(cur_clients[active_client_id].obj, message_type + msg)


    elif message_type == 'x':

        copyserver_id = int(msg[0])
        # now initiate a connection with the client's copyserver
        if copyserver_id == 0:
            client_copyserver_addr = "0.0.0.0:9001"
        elif copyserver_id == 1:
            client_copyserver_addr = "0.0.0.0:9002"
        elif copyserver_id == 2:
            client_copyserver_addr = "0.0.0.0:9003"

        connect_message = "hello"

        ws_copyserver = create_copyserver_socket(connect_message, client_copyserver_addr)

        cur_copyservers[copyserver_id] = ws_copyserver

    elif message_type == "v":
        clipboard = msg




def send_state_to_clients():
    pass

def client_left(client, server):
    global cur_clients, active_client_id
    for k,v in cur_clients.items():
        if v.client_obj == client:
            del cur_clients[k]
            if active_client_id == k:
                active_client_id = 0
                # This function should simply be the reply at every poll request: send_state_to_clients()   
            print("this is bad. client dead. ABORT ABORT.")
            return


def new_client(client, server):
    pass

if __name__ == "__main__":
    start_server()