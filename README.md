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

def handle_welcome(client, data): 
    print("The server welcomed me: %s" % data["msg"])
    client.rpc("thanks", {"msg": "Thanks for having me simplerpc"})

def handle_connect():
    print("Client connected on: %s:%s" % (TCP_IP, TCP_PORT))

def handle_disconnect():
    print("Client disconnected")

def handle_fail(data):
    print("RCP Failure %s -> %s" % (data["reason"], data["message"]))

client.handler.on("welcome", handle_welcome)
client.on_connect(handle_connect)
client.on_disconnect(handle_disconnect)
client.on_fail(handle_fail)
client.start() # blocking loop

```

#### Exceptions

On the server, if an Exception is raised, it's type and message will be caught and sent with the protocol FAIL rpc. 

```py

# callback for rpc "some_rpc"
def handle_some_rpc(conn, op, data):
    # this will be send using failure protocol
    # 'FAIL{"reason":"ValueError", "message":"Expected argument 'argname' in RPC: 'test'"}'
    if 'test' not in data:
        raise ValueError("Expected argument 'argname' in RPC: 'test'")

    # ...
```

## Protocol

Payloads strings take the form:

`OPNAME{"json": "data"}`

These are separated by newlines ('\n'). They are extracted and sent to a handler along with the Connection/Client object that received them. A handler is a callable with signature:

`(connection, opcode, data)`

**Failure**. Reserved for the protocol is the 'FAIL' message. This is a message notifying the client of a failed request. See exceptions above. It takes the form.

`FAIL{"reason": "FailureType", "message": "Some explanation"}`

## Installation

Clone the GIT repo and run `pip install .`

## TODO

- Logging
- Unit tests
- Explore 'threading' for non blocking dispatcher loops
