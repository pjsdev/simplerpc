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
- Move to text opcodes
- Explore 'threading' for non blocking dispatcher loops
