import os
import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration



DATAGRAM_SIZE = 1380

ADDRESS = "localhost"
PORT = 4433


class QuicServer (QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = open("receivedfile", "ab")
        self.bytes_received = 0



    def quic_event_received(self, event):
        # print('Server got:', event)
        if (event.__class__.__name__ == "StreamDataReceived"):
            self.bytes_received += len(event.data)
            self.file.write(event.data)
            print(self.bytes_received)



async def run_server():
    print("Starting Server")
    config = QuicConfiguration(
        is_client = False,
        max_datagram_size = DATAGRAM_SIZE,
        alpn_protocols = ['h3-29'],
        max_data = 999999999,
        max_stream_data = 999999999,
    )
    config.load_cert_chain(
        './aioquic-main/tests/ssl_cert.pem',
        './aioquic-main/tests/ssl_key.pem',
    )
    await serve (
        ADDRESS,
        PORT,
        create_protocol = QuicServer,
        configuration = config,
    )
    await asyncio.Future()


async def main():
    await asyncio.gather(
        run_server()
    )

asyncio.run(main())

