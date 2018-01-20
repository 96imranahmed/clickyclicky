# -*- coding: utf-8 -*-
from __future__ import print_function

from websocket_server import WebsocketServer

PORT = 9000
server = WebsocketServer(PORT, '0.0.0.0')

cur_clients = {}
client_dims = {}

active_screen_id = 0

def start_server():
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()

def message_received(client, server, message):
    global cur_clients, client_dims, active_screen_id

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
            cur_clients['master'] = client

        elif msg_lst[1] == "1":
        	slave_id = msg_lst[0]
        	print("Got slave connected")
        	cur_clients['slave_%d' % (slave_id,)] = client

        machine_id = msg_lst[0]

        client_dims[machine_id] = [int(i) for i in msg_lst[2].split(',')]

        server.send_message(client, "k")

    elif message_type == 'u':
    	msg_lst = msg.split(':')
    	# firstly get the new active screen
    	active_screen_id = int(msg_lst[0])

    	new_y = msg_lst[1]

    	# TODO Talk to the other client with this info
    	print("CONTEXT SWITCH TO %d" % active_screen_id)


    elif message_type == 'm':
    	coords = [int(i) for i in msg.split(',')]

    	# TODO TALK TO THE ACTIVE CLIENT with these coords
    	print("new coords for active client (%d, %d)" % (coords[0],coords[1]))

    elif message_type == 'l':
    	direction = int(msg)

    	# TODO TALK TO THE ACTIVE CLIENT with these coords
    	print("scroll boi for active client (%d)" % (direction))

    elif message_type == 'i':
    	msg_lst = msg.split(':')
    	action_type = int(msg_lst[0])
    	if action_type == 0:
    		# this is a key
    		print("SENDING KEY AND WHAT KEY")
    		# TODO Send to client
    	elif action_type == 1:
    		# this is a mouse action
    		print("SENDING mouse click/release")
    		# TODO

def client_left(client, server):
    global cur_clients
    for k,v in cur_clients.items():
    	if v == client:
    		del cur_clients[k]
    		print("this is bad. client dead. ABORT ABORT.")
    		return


def new_client(client, server):
    pass

if __name__ == "__main__":
    start_server()