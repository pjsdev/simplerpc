#! /usr/bin/env python

from simplerpc.server import Server
from simplerpc.client import Client
from simplerpc.handlers.messenger import Messenger
from simplerpc.util import Util

TCP_IP = '127.0.0.1'
TCP_PORT = 8000

Util.set_message_size(256)

n = None

def main_client():
    msg = Messenger()
    client = Client(TCP_IP, TCP_PORT, msg)

    def func(conn, args):
        print("--- func", args)
        if raw_input("send again? y/n") == "y":
            client.rpc(1, {"hello": "world"})

    def handle_connect():
        print("--- connected")

    def handle_disconnect():
        print("--- disconnected")

    client.on_connect(handle_connect)
    client.on_disconnect(handle_disconnect)

    msg.on(0, func)

    return client

def main_server():
    msg = Messenger()
    server = Server(TCP_IP, TCP_PORT, msg)

    def func(conn, args):
        print("*** func---> ", args)
        server.rpc(n, 0, {"single": "rpc"})
        server.rpc_all(0, {"all": "rpc"})

    def handle_connect(net_id):
        print("***", net_id)
        global n
        n = net_id
        server.rpc(n, 0, {"single": "rpc"})

    def handle_disconnect(net_id):
        print("***", net_id)

    server.on_connect(handle_connect) # fires(net_id)
    server.on_disconnect(handle_disconnect) # fires(net_id)

    msg.on(1, func) # fires(net_id, args)

    return server

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 0 :
        try:
            dispatcher = None
            if sys.argv[1] == "s":
                dispatcher = main_server()
            elif sys.argv[1] == "c":
                dispatcher = main_client()

            dispatcher.start()
        except KeyboardInterrupt:
            pass

        finally:
            # dispatcher.close()
            pass
    else:
        print("Usage: main.py s|c")
