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

def handle_client(conn, addr):
    print('thread starting...')
    print('TCP echo server accepted connection from', addr)

    received_bytes = 0

    while True:
        try: 
            data = conn.recv(10240)
            if len(data):
                received_bytes += len(data)
                print(received_bytes)
        except:
            print('An error occurred at server.')
            break

    
    conn.close()
    print('thread ending...')
    sys.exit()


# run TCP file server
def run_file_server():
    utils.kill_process_on_port(ECHO_SERVER_PORT)

    sock.bind(('', ECHO_SERVER_PORT))
    sock.listen(5)
    print('Ready to serve...')

    while True:
        # Establish the connection
        conn, addr = sock.accept()

        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()


def main():
    run_file_server()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sock.close()
        for t in all_threads:
            t.join()

        sys.exit()























