



# modify these addresses as needed
from utils import local_ip
proxy_addr = ("ms0403.utah.cloudlab.us", 4433)
echo_addr = ('ms0429.utah.cloudlab.us', 12345)
# local_addr is assigned dynamically

'''
Run echo server on a machine with Python and public IP address:

cd ~
rm -rf ~/masque-linux
sudo git clone https://github.com/dx2102/masque-linux
cd ~/masque-linux
sudo chmod a+rwx -R .
clear
python3 echo_server.py
(or python3 echo_server.py --quiet)




Run masquerade on a linux x86 machine with public IP address:
rm -rf ~/masque-linux
sudo git clone https://github.com/dx2102/masque-linux
cd ~/masque-linux
sudo chmod a+rwx -R .
clear

ifconfig -a
export RUST_LOG=debug
./server 0.0.0.0:4433
'''
None
import time
import os
import socket
import threading
import queue
import asyncio
loop = asyncio.get_event_loop()
import aioquic

import matplotlib.pyplot as plt

from utils import start
class Connection:
    '''
    This is an abstract base class for connections.
    We will implement four subclasses:
    - SimpleQueue()
    - LocalUDP()
    - DirectUDP()
    - DirectTCP()
    - MasqueUDP()
    - MasqueTCP()
    They will use global variables: masque_addr, echo_addr
    For simplicity, this class is synchronous.
    TCP connections will use \n as separator.
    '''
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
    async def send(self, data: bytes):
        raise NotImplementedError
    
    async def recv(self) -> bytes:
        raise NotImplementedError
async def benchmark(
        conn, experiment_name = 'experiment',
        payload = '', n = 100, gap = 0.01
    ):
    '''
    Benchmark any Connection object.
    Concatenate current time and a space to data, and send it n times.
    Record delays of each packet.
    Plot the result and save data to ./results/experiment_name.csv
    '''
    delays = {}
    async def recv():
        print('recv started')
        for i in range(n):
            data = (await conn.recv()).decode()
            print('received', data)
            # split with the first space
            recv_time = time.time()
            send_time, data = data.split(' ', 1)
            send_time = float(send_time)
            delay = recv_time - send_time
            if send_time not in delays:
                raise Exception(
                    'Received a packet that was not sent: ',
                    send_time, delays
                )
            if delays[send_time] is not None:
                raise Exception(
                    'Received a packet that was already received: ',
                    send_time, delays
                )
            delays[send_time] = delay
            # print(send_time % 1, recv_time % 1, delay % 1, delays)
    async def send():
        for i in range(n):
            send_time = time.time()
            data = (str(send_time) + ' ' + payload).encode()
            await conn.send(data)
            delays[send_time] = None
            await asyncio.sleep(gap)

    # only wait until send is done, then wait for 0.5 seconds
    # all packets that have not arrived will be assumed lost
    task = asyncio.create_task(recv())
    await send()
    await asyncio.sleep(0.5)

    if not os.path.exists('./results'):
        os.makedirs('./results')

    # csv
    file = open(f'./results/{experiment_name}.csv', 'w')
    file.write('send_time, delay\n')
    for send_time, delay in delays.items():
        file.write(f'{send_time}, {delay}\n')
    file.close()
    
    # plot
    print(delays)
    delays_lst = [delay 
        for send_time, delay in sorted(delays.items())]
    print(delays_lst)
    plt.plot(delays_lst)
    # red spots are lost packets
    lost_idx = [i for i, delay in enumerate(delays_lst) if delay is None]
    plt.scatter(lost_idx, [0 for i in lost_idx], c='r', s=3)
    plt.show()
    plt.savefig(f'./results{experiment_name}.png')
    await asyncio.sleep(0.1)

class SimpleQueue(Connection):
    '''
    This is a simple queue that can be used to test the benchmark function.
    '''
    def __init__(self, *args, **kwargs):
        self.queue = asyncio.Queue()
    
    async def send(self, data: bytes):
        await self.queue.put(data)
    
    async def recv(self) -> bytes:
        result = await self.queue.get()
        return result
    
asyncio.run(benchmark(
    SimpleQueue(), 'simple_queue', 
    payload='hello world', 
))
