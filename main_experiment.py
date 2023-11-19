import time
import os
import threading
import socket
import sys
import subprocess
import utils

SERVER_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
all_threads = []

def handle_client(conn, addr):
    print('thread starting...')
    print('TCP echo server accepted connection from', addr)

    startTime = time.time()

    while True:
        try: 
            data = conn.recv(1024)
            if len(data):
                print('TCP echo server received:', data)
                conn.send(data)
                startTime = time.time()
            if (time.time() - startTime >= 15):
                break
        except:
            print('An error occurred at server.')
            break

        time.sleep(1)
    
    conn.close()
    print('thread ending...')
    sys.exit()


# 启动UDP echo server
# @start
def run_server():
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', SERVER_PORT))
    sock.listen(5)
    print('Ready to serve...')

    while True:
        # Establish the connection
        conn, addr = sock.accept()

        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

# 启动TCP client，向masquerade client (8989端口)发起http代理的连接
# @start
def tcp_client(server_ip, client_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((client_ip, 8989))
    def send(data):
        sock.send(data.encode() + b'\r\n')
        print('TCP client sent: ', data)
    '''
    CONNECT /something/127.0.0.1/12345/ HTTP/1.1
    Host: example.com
    '''
    send(f'CONNECT {server_ip}:12345/ HTTP/1.1')
    send(f'Host: {server_ip}:12345')
    send('')
    send('hello')
    # 看看有没有得到echo
    data = sock.recv(1024)
    print('TCP client received: ', data)

def main():
    role = sys.argv[1]

    if (role == 'server'):
        run_server()

    elif (role == 'proxy'):
        utils.kill_process_on_port(8989)

        # server_ip = sys.argv[2]
        # proxy_ip = sys.argv[3]

        # 启动masquerade server
        # 结尾带&的命令会在后台运行
        utils.exec(f'''
        cd ~/masque-linux
        export RUST_LOG=info
        ./server {server_ip}:4433 &
        ''')

    elif (role == 'client'):
        proxy_ip = sys.argv[2]
        client_ip = sys.argv[3]

        # 启动masquerade client
        utils.exec(f'''
        cd ~/masque-linux
        export RUST_LOG=info
        ./client {proxy_ip}:4433 {client_ip}:8989 http &
        ''')

        tcp_client(proxy_ip, client_ip)
    else:
        raise ValueError('Unrecognized role')

    # time.sleep(999)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sock.close()
        for t in all_threads:
            t.join()

        sys.exit()























