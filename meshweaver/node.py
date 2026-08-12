import asyncio
import socket


class MeshNode:
    def __init__(self, host="127.0.0.1", port=0):
        self.host = host
        self.port = port
        self.transport = None

    async def start(self):
        loop = asyncio.get_running_loop()

        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: MeshProtocol(self),
            local_addr=(self.host, self.port)
        )

        # Get the actual port when port=0
        self.port = self.transport.get_extra_info("sockname")[1]

        print(f"Node started at {self.host}:{self.port}")

    async def ping(self, host, port):
        message = b"PING"

        self.transport.sendto(message, (host, port))
        print(f"PING sent to {host}:{port}")

    def stop(self):
        if self.transport:
            self.transport.close()
            print(f"Node {self.port} stopped")


class MeshProtocol(asyncio.DatagramProtocol):
    def __init__(self, node):
        self.node = node

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()

        print(f"Received '{message}' from {addr}")

        if message == "PING":
            self.transport.sendto(b"PONG", addr)
            print(f"PONG sent to {addr}")

        elif message == "PONG":
            print(f"PONG received from {addr}")