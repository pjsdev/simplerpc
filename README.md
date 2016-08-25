# simplerpc
A super lightweight bi-directional json rpc server in python.

## How to use

#### Simple messenger server 
```py
from simplerpc.server import Server
from simplerpc.handlers.message_handler import MessageHandler

msg = MessageHandler()
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
from simplerpc.handlers.message_handler import MessageHandler

msg = MessageHandler()
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

The message size must be set before starting the server. This is the persistent default for the server. If your application needs varying message sizes, a 'message size' protocol rpc can be sent with the new value

```py
from simplerpc.config import Config
Config.set_message_size(256) # must be done before start() called on dispatcher
```

#### Exceptions

In `simplerpc.exceptions` there are some useful exceptions including: ArgumentTypeError, ArgumentValueError, ArgumentMissing. When raised from a handler of associated callbacks, will end the handle and send a failure to the client.

```py
from simplerpc.exceptions import ArgumentMissing

# somewhere in my handler / callbacks
# this will be send using failure protocol
# '-1{"reason":"ArgumentMissing", "message":"Expected argument 'argname' in opcode 0"}'
raise ArgumentMissing("Expected argument 'argname' in opcode 0")
```

## Protocol

Payloads are a fixed sized strings of the form:

`11{"json": "data"}`

Where the leading number is an opcode and the rest is json data

These are extracted and sent to a handler along with the Connection/Client object that received them. A handler is a callable with signature:

`(connection, opcode, data)`

Negative opcodes are reserved for protocol codes, see below

**Failure**. A message notifying the client of a failed request

`(-1, {"reason": "FailureType", "message": "Some explanation"})`

**Message size**. A message sent when a client connects to tell them how big each message is in bytes:

`(-2, {"message_size": 256})`

## Installation

Clone the GIT repo and run `pip install .`

## TODO

- Logging
- Unit tests
- Explore 'threading' for non blocking dispatcher loops
- Keep an eye on message size feature. It is currently quite inflexible