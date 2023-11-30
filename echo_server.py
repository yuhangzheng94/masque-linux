

# 同时在0.0.0.0:12345运行udp和tcp的echo server
# 在udp中，每收到一个数据包，就回复一个数据相同的数据包
# 在tcp中，收到的字节串会被按照ascii中的换行(\n)分割，每收到一行，就回复一行
# 如果不发送换行，tcp echo server永远不会回复！

# 如果运行的时候使用了-q或者--quiet参数，那么就只打印连接者信息，不打印每次收到的数据


import socket
import argparse
import time
import threading
import sys

# start装饰器会在新线程，直接运行被装饰的函数
from utils import start, local_ip, kill_process_on_port
kill_process_on_port(12345)
print()
print('Running echo server on ' + local_ip + ':12345')

# 获取quiet
parser = argparse.ArgumentParser()
parser.add_argument('-q', '--quiet', action='store_true')
args = parser.parse_args()
quiet = args.quiet

def log(*args, **kwargs):
    if not quiet:
        print(*args, **kwargs)

@start
def tcp_echo_server():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('0.0.0.0', 12345))
    listener.listen()
    print('tcp echo server started')
    while True:
        conn, addr = listener.accept()
        print('tcp connected by', addr)
        @start
        def handler():
            while True:
                try:
                    data = conn.recv(1024)
                except ConnectionResetError:
                    break
                if not data:
                    break
                log('echoing to', addr, 'data:', data)
                conn.sendall(data)
            print('tcp connection closed by', addr)
            conn.close()

@start
def udp_echo_server():
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.bind(('0.0.0.0', 12345))
    print('udp echo server started')
    old_users = set()
    while True:
        try:
            data, addr = listener.recvfrom(1024)
        except ConnectionResetError as e:
            print(e)
            continue
        if addr not in old_users:
            print('new udp sender:', addr)
            old_users.add(addr)
        log('echoing udp to', addr, 'data:', data)
        listener.sendto(data, addr)


'''

# sends "hello" to localhost:12345 with udp
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"hello", ("localhost", 12345))
sock.close()


'''






























