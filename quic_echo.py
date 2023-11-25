

import time

import asyncio
import ssl
import aioquic

from aioquic.quic.connection import QuicConnection
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3Connection
from aioquic.quic.events import QuicEvent

from aioquic.asyncio.client import connect
from aioquic.asyncio.server import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol



class QuicEchoServer(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def quic_event_received(self, event):
        print('echo server got:', event)
        sort = event.__class__.__name__
        if sort == 'StreamDataReceived':
            print('echo server echoing')
            self._quic.send_stream_data(event.stream_id, event.data, False)

async def run_server():
    config = QuicConfiguration(
        is_client=False,      
        alpn_protocols=['h3-29'],     
    )
    config.load_cert_chain(
        './aioquic-main/tests/ssl_cert.pem',
        './aioquic-main/tests/ssl_key.pem',
    )

    await serve(
        'localhost', 4433, 
        create_protocol=QuicEchoServer,
        configuration=config,
    )
    await asyncio.Future()





class QuicEchoClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def quic_event_received(self, event):
        print('client got:', event)
    
    async def test(self):
        stream_id = self._quic.get_next_available_stream_id()
        for i in range(100):
            await asyncio.sleep(1)
            data = f'hello world {i}'.encode()
            print('\nclient sending')
            self._quic.send_stream_data(
                stream_id, 
                data,
                False
            )
            self.transmit()
            print('client sent:', data)
        await asyncio.sleep(999)

async def run_client():
    config = QuicConfiguration(
        is_client=True,
        alpn_protocols=['h3-29'],
    )
    config.load_verify_locations(
        './aioquic-main/tests/pycacert.pem',
    )
    async with connect(
        'localhost', 4433, 
        create_protocol=QuicEchoClient,
        configuration=config,
    ) as client:
        await client.test()
    await asyncio.Future()



async def main():
    await asyncio.gather(
        run_server(),
        run_client(),
    )

asyncio.run(main())












































