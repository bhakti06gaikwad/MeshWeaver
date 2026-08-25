import asyncio
import json
import uuid
from meshweaver.dht import KademliaDHT
from meshweaver.monitor import ResourceMonitor
from meshweaver.gossip import GossipManager
from meshweaver.scheduler import TaskScheduler

class MeshNode:
    def __init__(self, host="127.0.0.1", port=0):
      self.node_id = str(uuid.uuid4())
      self.host = host
      self.port = port
      self.transport = None
      self.running = False
      self.peers = {}

      self.dht = KademliaDHT(self.node_id)

      self.gossip = GossipManager(self)
      self.peer_metadata = {} 

      self.scheduler = TaskScheduler(self)

    def get_metadata(self):
        resources = self.get_resources()

        return {
            "node_id": self.node_id,
            "host": self.host,
            "port": self.port,
            "running": self.running,
            "peer_count": len(self.peers),
            "resources": resources,
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

    def add_dht_peer(self, node_id, host, port):
    #Add a peer to the DHT routing table.

       if node_id == self.node_id:
        return

       self.dht.add_node(node_id, host, port)

       print(
            f"DHT peer added: "
            f"{node_id} -> {host}:{port}"
        )


    def find_closest_peers(self, target_id, count=3):
    #Find peers closest to a target node ID.

        return self.dht.find_closest(
            target_id,
            count
        )
    
    def send_message(self, message, host, port):
    #Send a JSON message to another node.

        if not self.transport:
            print("Cannot send message: node is not running")
            return

        data = json.dumps(message).encode("utf-8")
        self.transport.sendto(data, (host, port))


    async def join_peer(self, host, port):
        #Ask an existing node to introduce us to the mesh.

        message = {
            "type": "JOIN",
            "node_id": self.node_id,
            "host": self.host,
            "port": self.port,
        }

        self.send_message(message, host, port)

        print(f"JOIN request sent to {host}:{port}")
    def get_resources(self):
    # Return current resource usage.

        return ResourceMonitor.get_resources()

    def gossip_to_peer(self, host, port):
    # Send this node's metadata to another node.

        if not self.running or not self.transport:
            print("Cannot gossip: node is not running")
            return

        data = self.gossip.encode_message()

        self.transport.sendto(
            data,
            (host, port)
        )

        print(f"GOSSIP sent to {host}:{port}")

    def select_task_node(self):
    #Select the best node for a task.

        selected = self.scheduler.select_node()

        if selected:
            print(
                f"Selected node: "
                f"{selected['node_id']} "
                f"(CPU={selected['cpu_percent']}%, "
                f"RAM={selected['memory_percent']}%)"
            )
        else:
            print("No suitable node found")

        return selected

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

        elif message_type == "JOIN":
            self.handle_join(message, addr)

        elif message_type == "PEERS":
            self.handle_peers(message)

        elif message_type == "GOSSIP":
            self.handle_gossip(message, addr)

        elif message_type == "PONG":
            print(f"PONG received from {addr}")

        else:
            print(f"Unknown message type: {message_type}")

    def handle_join(self, message, addr):
    #Handle a node requesting to join the mesh.

        node_id = message.get("node_id")
        host = message.get("host")
        port = message.get("port")

        if not node_id or not host or not port:
            print("Invalid JOIN request")
            return

        # Add joining node to our peer table
        self.node.add_peer(node_id, host, port)

        # Add joining node to DHT
        self.node.add_dht_peer(node_id, host, port)

        print(
            f"Node {node_id} joined from "
            f"{host}:{port}"
        )

        # Send our own information + known peers
        peers = [
            {
                "node_id": self.node.node_id,
                "host": self.node.host,
                "port": self.node.port,
            }
        ]

        for peer in self.node.get_peers():

            # Don't send the joining node back to itself
            if peer["node_id"] == node_id:
                continue

            peers.append({
                "node_id": peer["node_id"],
                "host": peer["host"],
                "port": peer["port"],
            })

        response = {
            "type": "PEERS",
            "sender": self.node.node_id,
            "peers": peers,
        }

        self.transport.sendto(
            json.dumps(response).encode("utf-8"),
            addr
        )

        print(f"Sent {len(peers)} peers to {addr}")

    def handle_peers(self, message):
        #Handle peers received from another node.

        peers = message.get("peers", [])

        print(f"Received {len(peers)} peers")

        for peer in peers:
            node_id = peer.get("node_id")
            host = peer.get("host")
            port = peer.get("port")

            if not node_id or not host or not port:
                continue

            # Don't add ourselves
            if node_id == self.node.node_id:
                continue

            # Add to peer table
            self.node.add_peer(
                node_id,
                host,
                port
            )

            # Add to DHT
            self.node.add_dht_peer(
                node_id,
                host,
                port
            )

        print(
            f"Peer discovery complete. "
            f"Known peers: {len(self.node.peers)}"
        )
    def handle_gossip(self, message, addr):
    #Process resource information received from another node.

        sender = message.get("sender")
        metadata = message.get("metadata")

        if not sender or not metadata:
            print("Invalid GOSSIP message")
            return

        self.node.peer_metadata[sender] = metadata

        print(
            f"GOSSIP received from {sender} "
            f"at {addr}"
        )

        resources = metadata.get("resources", {})

        print(
            f"Peer resources: "
            f"CPU={resources.get('cpu_percent')}%, "
            f"RAM={resources.get('memory_percent')}%"
        )