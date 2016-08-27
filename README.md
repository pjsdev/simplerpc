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

# every connection that sends this rpc, will trigger the CB
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
    client.rpc("thanks", {"msg": "Thanks for having me simple"})

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

In `simplerpc.exceptions` there are some useful exceptions including: ArgumentTypeError, ArgumentValueError, ArgumentMissing. When raised from a handler of associated callbacks, will end the handle and send a failure to the client.

```py
from simplerpc.exceptions import ArgumentMissing

# somewhere in my handler / callbacks
# this will be send using failure protocol
# 'FAIL{"reason":"ArgumentMissing", "message":"Expected argument 'argname' in RPC: 'test'"}'
raise ArgumentMissing("Expected argument 'argname' in RPC: 'test'")
```

## Protocol

Payloads strings of the form separated by '\n':

`OPNAME{"json": "data"}`

These are extracted and sent to a handler along with the Connection/Client object that received them. A handler is a callable with signature:

`(connection, opcode, data)`

**Failure**. A message notifying the client of a failed request, FAIL is reserved for protocol

`FAIL{"reason": "FailureType", "message": "Some explanation"}`

## Installation

Clone the GIT repo and run `pip install .`

## TODO

- Logging
- Unit tests
- Consider server/connection level handlers & forwarding
- Explore 'threading' for non blocking dispatcher loops
