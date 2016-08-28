#! /usr/bin/env python

from simplerpc.server import Server
from simplerpc.client import Client
from simplerpc.handlers.message_handler import MessageHandler

TCP_IP = '127.0.0.1'
TCP_PORT = 8000

def main_client():
    client = Client(TCP_IP, TCP_PORT, MessageHandler())

    def handle_welcome(client, data): 
        print("The server welcomed me: %s" % data["msg"])
        client.rpc("thanks", {"msg": "Thanks for having me simplerpc"})
        client.rpc("thanks", {"msg": "This time with a callback"}, handle_res)

    def handle_connect():
        print("Client connected on: %s:%s" % (TCP_IP, TCP_PORT))

    def handle_disconnect():
        print("Client disconnected")

    def handle_all_fails(data):
        print("RCP Failure %s -> %s" % (data["reason"], data["message"]))

    def handle_res(conn, opname, data):
        print("Response received", opname, data)

    client.handler.on("welcome", handle_welcome)
    client.handler.on("FAIL", handle_all_fails)
    client.on_connect(handle_connect)
    client.on_disconnect(handle_disconnect)
    
    return client

def main_server():
    server = Server(TCP_IP, TCP_PORT, MessageHandler())
    print("TCP Server listening on %s:%s" % (TCP_IP, TCP_PORT))

    def handle_thanks(connection, data):
        print("The client showed gratitude: %s" % data["msg"])
        connection.okay_data = {"Custom OKAY data": 123}

    def handle_connect(connection):
        print("Client connected with net id: %s" % connection.net_id)
        connection.rpc("welcome", {"msg": "Welcome to simplerpc"})

    def handle_disconnect(net_id):
        print("Disconnect: %s" % net_id)

    # every connection that sends this rpc, will trigger the CB
    server.handler.on("thanks", handle_thanks)
    server.on_connect(handle_connect)
    server.on_disconnect(handle_disconnect)

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
            if dispatcher:
                dispatcher.close()
    else:
        print("Usage: sample.py s|c")
