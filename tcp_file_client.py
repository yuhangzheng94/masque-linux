import time
import os
import threading
import socket
import sys
import utils

ECHO_SERVER_PORT = 12345
MASQUE_SERVER_PORT = 4433
MASQUE_CLIENT_PORT = 8989
LOG_LEVEL = 'debug'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
all_threads = []

file = open("testfile", "rb")


def test_file_client(server_ip, client_ip):

    sock.connect((client_ip, MASQUE_CLIENT_PORT))
    def send(data):
        sock.send(data.encode() + b'\r\n')
        print('TCP client sent: ', data)
    '''
    CONNECT /something/127.0.0.1/12345/ HTTP/1.1
    Host: example.com
    '''
    send(f'CONNECT {server_ip}:{ECHO_SERVER_PORT}/ HTTP/1.1')
    send(f'Host: {server_ip}:{ECHO_SERVER_PORT}')
    time.sleep(0.1)

    # Send File
    data = file.read()
    sock.send(data)

    time.sleep(5)

    file.close()
    sock.close()

def main():
    server_ip = sys.argv[1]
    client_ip = sys.argv[2]

    test_file_client(server_ip, client_ip)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        file.close()

        sock.close()
        for t in all_threads:
            t.join()

        sys.exit()























