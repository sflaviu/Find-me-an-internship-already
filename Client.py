#!C:/Python34/python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.43.112', 1234)
print("connecting to %s port %d" % server_address)
sock.connect(server_address)

try:
    message = "Hello Eneia, how was your day? Had fun with Prism??"
    print("seding message: %s" % message)
    sock.sendall(message.encode())

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print("received %s " % data)

finally:
    print("Closing socket")
    sock.close()