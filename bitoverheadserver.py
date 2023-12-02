import os
import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration

DATAGRAM_SIZE = 1280

class QuicServer(QuicConnectionProtocol):
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
    config = QuicConfiguration(
        is_client = False,
        max_datagram_size = DATAGRAM_SIZE,
        alpn_protocols = ['h3-29'],
        max_data=10000000000,
        max_stream_data=10000000000,
    )
    config.load_cert_chain(
        './aioquic-main/tests/ssl_cert.pem',
        './aioquic-main/tests/ssl_key.pem',
    )

    await serve(
        'localhost', 4433,
        create_protocol = QuicServer,
        configuration = config,
    )
    await asyncio.Future()


async def main():
    await asyncio.gather(
        run_server()
    )

asyncio.run(main())

# if __name__ == "__main__":
#     asyncio.run(main())
