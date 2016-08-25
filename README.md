# simplerpc
A super lightweight bi-directional json rpc server in python.

## How to use

#### Simple messenger server 
```py
from simplerpc.server import Server
from simplerpc.handlers.messenger import Messenger

msg = Messenger()
server = Server('127.0.0.1', 30000, msg)

def handle_0(connection, data):
    print("Got RPC 0 with : %s" % data)

def handle_connect(connection):
    # send RPC to connection three times
    server.rpc_all(1, {"some_data": "this is sent to every connection"})
    server.rpc(
        connection.net_id, 1, 
        {"some_data": "this is sent to whoever just connected"}
    )
    connection.rpc(1, {"some_data": "this is sent to whoever just connected"})

msg.on(0, handle_0)
server.on_connect(handle_connect)
server.on_disconnect(handle_disconnect) # callback omitted
server.start() # blocking loop

```

#### Simple messenger client
```py
from simplerpc.client import Client
from simplerpc.handlers.messenger import Messenger

msg = Messenger()
client = Client('127.0.0.1', 30000, msg)

def handle_1(connection, data): # connection here is the client
    print("Got RPC 1 with : %s" % data)
    connection.rpc(0, {"some_data": 123})

msg.on(1, handle_1)
client.on_connect(handle_connect) # callback omitted
client.on_disconnect(handle_disconnect) # callback omitted
client.on_fail(handle_fail) # callback omitted
client.start() # blocking loop

```

#### Change Message Size
```py
from simplerpc.config import Config
Config.set_message_size(256) # must be done before start() called on dispatcher
```

#### Exceptions
```py
from simplerpc.exceptions import ArgumentMissing

# somewhere in my handler / callbacks
# this will be send using failure protocol
# '-1{"reason":"ArgumentMissing", "message":"Expected argument 'argname' in opcode 0"}
raise ArgumentMissing("Expected argument 'argname' in opcode 0")
```

## Protocol

Payloads are a fixed sized strings of the form:

    `11{"json": "data"}`

Where the leading number is an opcode and the rest is json data

These are extracted and sent to a handler along with the Connection/Client object that received them. A handler is a callable with signature:

`(connection, opcode, data)`

Negative opcodes are reserved for protocol codes, see below

Failure
    `(-1, {"reason": "FailureType", "message": "Some explanation"})`

Message size, sent on client connect
    `(-2, {"message_size": 256})`

## Installation

Clone the GIT repo and run `pip install .`

## TODO

- Logging
- Unit tests
- Commenting
- Explore 'threading'
- Resolve base class clashes from server/client/connection