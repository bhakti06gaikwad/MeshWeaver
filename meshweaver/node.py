import asyncio
import json
import uuid

class MeshNode:
    def __init__(self, host="127.0.0.1", port=0):
      self.node_id = str(uuid.uuid4())
      self.host = host
      self.port = port
      self.transport = None
      self.running = False

    
    def get_metadata(self):
        return {
            "node_id": self.node_id,
            "host": self.host,
            "port": self.port,
            "running": self.running,
        }

    async def start(self):
        if self.running:
            print(f"Node {self.port} is already running")
            return

        loop = asyncio.get_running_loop()

        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: MeshProtocol(self),
            local_addr=(self.host, self.port)
        )

        self.port = self.transport.get_extra_info("sockname")[1]
        self.running = True

        print(f"Node started at {self.host}:{self.port}")

    async def ping(self, host, port):
        if not self.running or self.transport is None:
            print("Cannot send PING: node is not running")
            return

        message = {
            "type": "PING",
            "sender": f"{self.host}:{self.port}"
        }

        data = json.dumps(message).encode("utf-8")

        self.transport.sendto(data, (host, port))

        print(f"PING sent to {host}:{port}")

    def stop(self):
        if not self.running:
            print("Node is already stopped")
            return

        if self.transport:
            self.transport.close()
            self.transport = None

        self.running = False

        print(f"Node {self.port} stopped")


class MeshProtocol(asyncio.DatagramProtocol):

    def __init__(self, node):
        self.node = node
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            message = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            print(f"Invalid message received from {addr}")
            return

        message_type = message.get("type")

        print(
            f"Received {message_type} "
            f"from {message.get('sender')} at {addr}"
        )

        if message_type == "PING":
            response = {
                "type": "PONG",
                "sender": f"{self.node.host}:{self.node.port}"
            }

            self.transport.sendto(
                json.dumps(response).encode("utf-8"),
                addr
            )

            print(f"PONG sent to {addr}")

        elif message_type == "PONG":
            print(f"PONG received from {addr}")

        else:
            print(f"Unknown message type: {message_type}")