# simplerpc
A super lightweight bi-directional json rpc server in python.

## How to use

#### Simple messenger server 
```py
from simplerpc.server import Server
from simplerpc.handlers.message_handler import MessageHandler

server = Server('127.0.0.1', 30000, MessageHandler())
print("TCP Server listening on %s:%s" % (TCP_IP, TCP_PORT))

def handle_thanks(connection, data):
    print("The client showed gratitude: %s" % data["msg"])

def handle_connect(connection):
    print("Client connected with net id: %s" % connection.net_id)
    connection.rpc("welcome", {"msg": "Welcome to simplerpc"})

def handle_disconnect(net_id):
    print("Disconnect: %s" % net_id)

# the server's handler will be copied to each connection
server.handler.on("thanks", handle_thanks)
server.on_connect(handle_connect)
server.on_disconnect(handle_disconnect)
server.start() # blocking loop

```

#### Simple messenger client
```py
from simplerpc.client import Client
from simplerpc.handlers.message_handler import MessageHandler

client = Client('127.0.0.1', 30000, MessageHandler())

def handle_res(conn, opname, data):
    print("Response received", opname, data)

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

client.handler.on("welcome", handle_welcome)
client.handler.on("FAIL", handle_all_fails)
client.on_connect(handle_connect)
client.on_disconnect(handle_disconnect)
client.start() # blocking loop

```

#### Exceptions

On the server, if an Exception is raised during RPC handling, it will be caught and sent with the protocol FAIL rpc as an unknown error. To send the client error information, inherit from `simplerpc.exceptions.SimpleRPCException` and raise your error from within the handler / callbacks

```py

# callback for rpc "some_rpc"
def handle_some_rpc(conn, op, data):
    # this will be send using failure protocol
    # 'FAIL{"reason":"MyCustomError", "message":"Expected argument 'argname' in RPC: 'test'"}'
    if 'test' not in data:
        raise MyCustomError("Expected argument 'argname' in RPC: 'test'")

    # ...
```

## Protocol

Payloads strings take the form:

`OPNAME{"json": "data"}`

These are separated by newlines ('\n'). They are extracted and sent to a handler along with the Connection/Client object that received them. A handler is a callable with signature:

`(connection, opcode, data)`

**Responses**. Reserved for the protocol are the 'FAIL' and 'OKAY' messages. These are messages considered 'responses' to each client RPC made. **FAIL*** is a message notifying the client of a failed request (see exceptions above). It takes the form.

`FAIL{"reason": "FailureType", "message": "Some explanation"}`

**OKAY** can be sent with arbitrary data from the server

## Installation

Clone the GIT repo and run `pip install .`

## TODO

- Logging
- Unit tests
- Explore 'threading' for non blocking dispatcher loops
