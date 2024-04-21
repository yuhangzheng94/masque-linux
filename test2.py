
# try to interact with the masquerade proxy server



import time
import os
import threading
import socket
import subprocess
import aioquic

# 为了debug我封装了一些函数...

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def path_exists(path):
    path = os.path.expanduser(path)
    return os.path.exists(path)

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



# 下载编译好的masquerade，保存在~/masque-linux
force_reinstall = False
if not path_exists('~/masque-linux') or force_reinstall:
    exec('''
        sudo apt update
        sudo apt install -y python3-pip libssl-dev
        pip install aioquic
        clear

        sudo rm -rf ~/masque-linux
        cd ~
        sudo git clone https://github.com/dx2102/masque-linux
        cd masque-linux
        sudo chmod +x server
        sudo chmod +x client 
    ''')
    time.sleep(4)

from aioquic.quic.connection import QuicConnection
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3Connection



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
    # 这里会遇到connection_id, stream_id, flow_id三个概念...

    # 我们只创建了一个quic_conn
    # 每个quic_conn拥有唯一一个connection id，
    # 而且只对应唯一的udp socket，
    # 除非触发connection migration(aioquic似乎还不支持)
    # 在建立connection的时候，会进行TLS握手实现加密

    # 同一个quic_conn内，可以创建多个quic stream
    # 每个stream有自己的stream id
    # 这就实现了在同一个udp socket上多路复用quic stream

    # 同一个quic_conn内，还可以直接收发quic datagram
    # quic datagram和stream的区别是，datagram不需要ACK和重发
    # 更类似直接通过udp通信
    # quic datagram不存在stream id或者flow id
    # ietf还定义了HTTP/3 DATAGRAM
    # HTTP/3 DATAGRAM会放在quic datagram中传输，
    # 每个HTTP/3 DATAGRAM开头有flow-id，随后是数据

    # 要创建http/3的connect-udp代理：
    # 1. 创建quic connection，随机分配connection-id，
    # 2. 创建quic stream，使用随机的stream-id，在其中写入http/3请求头，
    # 比如：
    # GET https://example.org/.well-known/masque/udp/192.0.2.6/443/ HTTP/1.1
    # Host: example.org
    # Connection: Upgrade
    # Upgrade: connect-udp
    # Capsule-Protocol: ?1
    # 3. 等待服务器回复200 OK，
    # 4. 开始发送HTTP3 DATAGRAM，其中flow_id = stream_id // 4
    # 这是因为之前的stream_id的最后两位，
    # 代表连接是单向还是双向、创建者是发送方还是接收方
    # 对于connect-udp，这两个信息是固定的，在flow-id中可以忽略





    proxy = ('localhost', 4433)
    target = ('localhost', 12345)

    quic_config = QuicConfiguration(
        is_client=True,
    )
    quic_config.load_verify_locations(
        os.path.expanduser("~/masque-linux/example_cert/cert.crt")
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
            print('sending {} bytes to {}', len(data), _addr)
            udp_sock.sendto(data, proxy)
        next_send_time = quic_conn.get_timer()
        print('next_send_time:', next_send_time)
        print('now:', time.time())
        if next_send_time is not None:
            @spawn
            def _():
                time.sleep(next_send_time - time.time())
                quic_conn.handle_timer(now=time.time())
                send()
    # recv()是自动运行的线程，把socket的数据读入quic_conn
    @spawn
    def recv():
        while True:
            data, addr = udp_sock.recvfrom(65535)
            print('received {} bytes from {}', len(data), addr)
            quic_conn.receive_datagram(data, proxy[0], now=time.time())
    
    quic_conn.connect(*proxy)
    send()














print('\n\n')
time.sleep(999999999)


































