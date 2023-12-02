import time
import os
import threading
import socket
import sys
import subprocess
import utils

ECHO_SERVER_PORT = 12345
MASQUE_SERVER_PORT = 4433
MASQUE_CLIENT_PORT = 8989
LOG_LEVEL = 'debug'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
all_threads = []

myFile = open("test/test98.txt", "a")

def test_echo_client(server_ip, client_ip):

    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    # 看看有没有得到echo
    for i in range(20):
        myFile.write(str(i)+",")
        t_sent = time.clock_gettime_ns(time.CLOCK_REALTIME)
        myFile.write(str(t_sent)+",")
        send(f'Hello world! #{i}')

        filetosend = open("lorem.txt", "r")
        data = filetosend.read(1024)
        while data:
            print("Sending...")
            send(data)
            data = sock.recv(1024)
            if data:
                print('TCP client received: ', data)
            data = filetosend.read(1024)
        filetosend.close()

        send('DONE')

        data = sock.recv(1024)
        # time.sleep(0.00001)
        while (not data.decode().strip().endswith('DONE')):
            print('TCP client received: ', data)
            data = sock.recv(1024)
        print('TCP client received: ', data)
        t_received = time.clock_gettime_ns(time.CLOCK_REALTIME)
        myFile.write(str(t_received)+",")
        print('TCP client received: ', data)

        diff = t_received - t_sent
        myFile.write(str(diff)+"\n")

    myFile.close()
    while (True):
        data = sock.recv(1024)
        if data:
            print('TCP client received: ', data)
    # sock.close()

def main():
    server_ip = sys.argv[1]
    client_ip = sys.argv[2]

    test_echo_client(server_ip, client_ip)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        myFile.close()

        sock.close()
        for t in all_threads:
            t.join()

        sys.exit()























