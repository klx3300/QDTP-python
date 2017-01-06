# QDTP-python
qDataTransportationProtocol(python implementation)

## Notice

### Network
Server runs on port 4582

### Drawbacks

No strict data correction check.

Creating folders not supported.

and *so many* features still not supported ...

### Communication Stream

C:Ask TCP connection

S:Receive TCP connection & waits for authentication information

C:Send Authentication string & waits for server result message.

S:Check Authentication string with local version.

S:On Success,return "Auth succ." On fail,return "Auth fail."

C:Send operation code.

[on operation get(code G)]

C:Send filename & Wait for server result return.

S:Try to open specified file.

S:Success "080 OK" fail "127 File not found."

S: Send file data with 256 bytes each.

S: Close connection.

[on operation set(code S)]

C:Send filename & wait for server result return.

S:Try to open specified file.

S:Success "080 OK" fail "290 Filesystem corruption or system resource fail."

C:Send file data with 256 bytes each.

C:Close connection.