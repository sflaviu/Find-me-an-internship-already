import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.43.112', 1234)
print('starting up on %s port %d' %server_address)
sock.bind(server_address)

sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from %s ' %client_address[0])

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print(data.decode("utf-8"))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no more data from %s '%client_address[0])
                break
    finally:
    # Clean up the connection
        connection.close()