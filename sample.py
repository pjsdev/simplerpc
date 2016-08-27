#! /usr/bin/env python

from simplerpc.server import Server
from simplerpc.client import Client
from simplerpc.handlers.message_handler import MessageHandler

from simplerpc import exceptions

TCP_IP = '127.0.0.1'
TCP_PORT = 8000

n = None

def main_client():
    msg = MessageHandler()
    client = Client(TCP_IP, TCP_PORT, msg)

    def func(conn, args):
        print("--- func", args)
        if raw_input("send again? y/n") == "y":
            conn.rpc("test_to_server", {"hello": "world"})

    def handle_connect():
        print("--- connected")

    def handle_disconnect():
        print("--- disconnected")

    def handle_fail(data):
        print("--- failure", data)

    client.on_connect(handle_connect)
    client.on_disconnect(handle_disconnect)
    client.on_fail(handle_fail)

    msg.on("test_to_client", func)

    return client

def main_server():
    msg = MessageHandler()
    server = Server(TCP_IP, TCP_PORT, msg)

    def func(conn, args):
        print("*** func---> ", args)
        raise exceptions.ArgumentMissing("Missing fake arg...")
        conn.rpc("test_to_client", {"single": "rpc"})

    def handle_connect(conn):
        print("*** connect", conn.net_id)
        conn.rpc("test_to_client", {"single": "rpc"})

    def handle_disconnect(net_id):
        print("*** disconnect", net_id)

    server.on_connect(handle_connect) # fires(net_id)
    server.on_disconnect(handle_disconnect) # fires(net_id)

    msg.on("test_to_server", func) # fires(net_id, args)

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
            dispatcher.close()
    else:
        print("Usage: sample.py s|c")
