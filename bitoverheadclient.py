import os
import asyncio
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration


DATAGRAM_SIZE = 1280

class QuicClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = open("testfile", "rb")




    async def send(self):
        print("Send File")
        stream_id = self._quic.get_next_available_stream_id()
        data = self.file.read()
        self._quic.send_stream_data(stream_id, data, False)
        self.transmit()
        await asyncio.sleep(999)



async def run_client():
    config = QuicConfiguration(
        is_client = True,
        max_datagram_size = DATAGRAM_SIZE,
        alpn_protocols=['h3-29'],
        max_data = 10000000000,
        max_stream_data = 10000000000,
    )
    config.load_verify_locations(
        './aioquic-main/tests/pycacert.pem',
    )
    async with connect (
        "localhost", 4433,
        configuration = config,
        create_protocol = QuicClient,
    ) as client:
        await client.send()
    await asyncio.Future()

async def main():
    await asyncio.gather(
        run_client(),
    )

asyncio.run(main())

# if __name__ == "__main__":
#     asyncio.run(main())
