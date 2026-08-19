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
      self.peers = {}

    
    def get_metadata(self):
        return {
            "node_id": self.node_id,
            "host": self.host,
            "port": self.port,
            "running": self.running,
            "peer_count": len(self.peers),
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

    def add_peer(self, node_id, host, port):
     #Add or update a peer.

      if node_id == self.node_id:
         return

      self.peers[node_id] = {
        "node_id": node_id,
        "host": host,
        "port": port,
        "status": "known",
      }

      print(f"Peer added: {node_id} -> {host}:{port}")


    def remove_peer(self, node_id):
      #Remove a peer from the peer table.

      if node_id in self.peers:
        del self.peers[node_id]
        print(f"Peer removed: {node_id}")


    def get_peers(self):
    # Return all known peers.

      return list(self.peers.values())


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