import DBConnection
import thread
import socket


def server_listen(socketus, connection1, client_address1):

    res = ""
    while True:
        data = connection1.recv(1)

        if not data or data.decode("utf-8") == "!":  # the message should end with "!" !! unless we change the means of
                                                    # communication
            break

        res += data.decode("utf-8")
    print(res)
    result = exec_query(res)
    connection1.sendall(result[0].userName)
    connection1.close()



def exec_query(allfunc):
    with lock:
        con = DBConnection.DBConnection()
        con.connect()

        parts = allfunc.split(";")  # put a semicolon ; after the first word (function name)
        func = parts[0]
        if len(parts) == 1:
            func = getattr(con, func)
            response = func()
            return response
        if len(parts) > 1:
            args = parts[1].split(":")  # put a colon : between function parameters
            func = getattr(con, func)
            response = func(*args)
            return response


lock = thread.allocate_lock()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('10.142.0.2', 1234)
print('starting up on %s port %d' % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    thread.start_new_thread(server_listen, (sock, connection, client_address))
