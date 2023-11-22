
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

def log(*args):
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    END = '\033[0m'
    print(BLUE + BOLD, end='')
    print(*args, end='')
    print(END, end='\n')
    time.sleep(0.01)

def exec(command):
    log('\n\n\nexecuting:', command)
    os.system(command)
    time.sleep(1/10)

def spawn(func):
    thread = threading.Thread(target=func)
    thread.start()

def start(func):
    log('\n\n\nstarting:', func.__name__)
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
                log(f"Terminated process with PID {pid}")
    except subprocess.CalledProcessError:
        log(f"No process found listening on port {port}")
    finally:
        time.sleep(wait)






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
    log('UDP echo server started')
    while True:
        data, addr = sock.recvfrom(1024)
        log('UDP echo server echoing: ', data)
        sock.sendto(data, addr)
    sock.close()



# 3. 启动aioquic masque client
# 通过 masque proxy server 访问 udp echo server
# aioquic提供了QuicConnection和H3Connection
# 但是它们只是状态机，
# 我们需要自己在UdpSocket, QuicConnection, H3Connection之间读写数据...


from aioquic.quic.connection import QuicConnection
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3Connection
from aioquic.quic.events import QuicEvent

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol

import asyncio
import ssl

class MasqueClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h3 = H3Connection(self._quic)

    def quic_event_received(self, event: QuicEvent):
        # 由于我们在手动管理self.h3状态机，必须保证它能收到所有的QuicEvent
        self.h3.handle_event(event)
        # 打印所有event
        sort = event.__class__.__name__
        if sort == 'StreamDataReceived':
            if event.stream_id % 4 == 3:
                log('drop GREASE noise on stream', event.stream_id)
                return
        log(event)
    
    async def test(self):
        log('sending connect-udp request')
        stream_id = self._quic.get_next_available_stream_id()
        self.h3.send_headers(
            stream_id=stream_id,
            headers=[
                (b":method", b"CONNECT"), # 和一般的GET POST等不同，masque代理的特殊标记
                (b":protocol", b"connect-udp"), # 另一个特殊标记，表示要用udp不是tcp
                (b":path", b"/well-known/masque/localhost/12345"), # 转发的目的地，实际上之后最后两个斜杠会被读取

                (b":authority", b"localhost"), # 代理服务器本身的地址，实际上并不会被masquerade检查
                (b":scheme", b"https"), # scheme允许在同一个连接中混用http和https，实际上也不会被masquerade检查
            ],
        )
        self.transmit()
        # 接下来要等待 200 OK，但是这里直接用sleep代替
        await asyncio.sleep(2)

        log('sending data to udp echo server')
        flow_id = stream_id // 4
        data = b'hello world'
        self.h3.send_datagram(flow_id, b'\x00' + data)
        self.transmit()

async def main():
    async with connect(
        'localhost', 4433, 
        create_protocol=MasqueClient,
        configuration=QuicConfiguration(
            is_client=True,
            verify_mode=ssl.CERT_NONE,
            alpn_protocols=["h3-29"],
        ),
    ) as client:
        await client.test()
        await asyncio.sleep(9999)

asyncio.run(main())











loop = asyncio.get_event_loop()
server = loop.create_datagram_endpoint(lambda: protocol, local_addr=(host, port))
transport, protocol = loop.run_until_complete(server)


































