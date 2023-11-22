
# try to interact with the masquerade proxy server


# The following script can download this script,
#   the required dependencies, and certificates,
'''
sudo apt update
sudo apt install -y python3-pip libssl-dev
pip install aioquic
clear

cd ~
sudo rm -rf ~/masque-linux
sudo git clone https://github.com/dx2102/masque-linux
cd masque-linux
sudo chmod a+rwx -R .
'''


import time
import os
import threading
import socket
import subprocess
import aioquic

def exec(command):
    print('\n\n\nexecuting:', command)
    os.system(command)
    time.sleep(1/10)

def spawn(func):
    thread = threading.Thread(target=func)
    thread.start()

def start(func):
    print('\n\n\nstarting:', func.__name__)
    thread = threading.Thread(target=func)
    thread.start()
    time.sleep(1/10)

def kill_process_on_port(port, wait=0.1):
    try:
        # 使用 lsof 命令查找监听指定端口的进程并获取其PID
        cmd = f"lsof -i :{port} -t"
        output = subprocess.check_output(cmd, shell=True)
        pids = output.decode('utf-8').split('\n')
        
        for pid in pids:
            if pid:
                pid = int(pid)
                # 终止进程
                subprocess.call(['kill', '-9', str(pid)])
                print(f"Terminated process with PID {pid}")
    except subprocess.CalledProcessError:
        print(f"No process found listening on port {port}")
    finally:
        time.sleep(wait)





from aioquic.quic.connection import QuicConnection
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3Connection
import ssl


# 1. 启动masquerade proxy server
kill_process_on_port(4433)
exec('''
cd ~/masque-linux
export RUST_LOG=debug
./server localhost:4433 &
''')



# 2. 启动udp echo server
@start
def udp_echo_server():
    # to test echo server in command line:
    # nc -u localhost 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 12345))
    print('UDP echo server started')
    while True:
        data, addr = sock.recvfrom(1024)
        print('UDP echo server echoing: ', data)
        sock.sendto(data, addr)
    sock.close()



# 3. 启动aioquic masque client
# 通过 masque proxy server 访问 udp echo server
# aioquic提供了QuicConnection和H3Connection
# 但是它们只是状态机，
# 我们需要自己在UdpSocket, QuicConnection, H3Connection之间读写数据...

@start
def aioquic_masque_client():

    proxy = ('localhost', 4433)
    target = ('localhost', 12345)

    quic_config = QuicConfiguration(
        is_client=True,
        verify_mode=ssl.CERT_NONE,
        alpn_protocols=["h3-29"],
    )
    quic_conn = QuicConnection(
        configuration=quic_config,
    )
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 为了支持不同的并发模型，
    # quic_conn h3_conn都只是状态机，
    # 我们需要自己实现计时、并发、读写udp socket

    # send()把quic_conn的数据写入socket，每次我们预期要发送数据时，都需要调用
    def send():
        for data, _addr in quic_conn.datagrams_to_send(now=time.time()):
            print(f'\nsending {len(data)} bytes to {_addr}')
            udp_sock.sendto(data, proxy)
        # next_send_time = quic_conn.get_timer()
        # print('next_send_time:', next_send_time)
        # print('now:', time.time())
        # if next_send_time is not None:
        #     @spawn
        #     def _():
        #         time.sleep(next_send_time - time.time())
        #         quic_conn.handle_timer(now=time.time())
        #         send()

    # 更好的办法是用timer
    @spawn
    def auto_send():
        while True:
            time.sleep(1)
            send()
    # 创建自动运行的线程，把socket的数据读入quic_conn
    @spawn
    def auto_recv():
        while True:
            data, addr = udp_sock.recvfrom(65535)
            print(f'\nreceived {len(data)} bytes from {addr}')
            quic_conn.receive_datagram(data, proxy[0], now=time.time())
    
    quic_conn.connect(*proxy)
    send()














time.sleep(999999999)


































