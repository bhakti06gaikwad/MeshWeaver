import json


class GossipManager:
    """Manage gossip messages between MeshWeaver nodes."""

    def __init__(self, node):
        self.node = node

    def create_message(self):
        """Create a gossip message containing node information."""

        return {
            "type": "GOSSIP",
            "sender": self.node.node_id,
            "metadata": self.node.get_metadata(),
        }

    def encode_message(self):
        """Encode the gossip message for network transmission."""

        message = self.create_message()

        return json.dumps(message).encode("utf-8")