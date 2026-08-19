import hashlib


class KademliaDHT:
    """
    Lightweight Kademlia-style routing table.

    This implementation provides:
    - node ID generation
    - XOR distance calculation
    - peer storage
    - closest-peer lookup
    """

    ID_BITS = 160

    def __init__(self, node_id):
        self.node_id = self._normalize_id(node_id)
        self.routing_table = {}

    @staticmethod
    def _normalize_id(node_id):
        """
        Convert a node identifier into a 160-bit integer.
        """

        if isinstance(node_id, int):
            return node_id

        digest = hashlib.sha1(
            str(node_id).encode("utf-8")
        ).hexdigest()

        return int(digest, 16)

    def distance(self, node_id):
        """
        Calculate XOR distance from this node to another node.
        """

        other_id = self._normalize_id(node_id)

        return self.node_id ^ other_id

    def add_node(self, node_id, host, port):
        """
        Add a node to the routing table.
        """

        node_key = str(node_id)

        self.routing_table[node_key] = {
            "node_id": node_key,
            "host": host,
            "port": port,
            "distance": self.distance(node_id),
        }

    def remove_node(self, node_id):
        """
        Remove a node from the routing table.
        """

        self.routing_table.pop(str(node_id), None)

    def find_closest(self, target_id, count=3):
        """
        Return the closest known nodes to the target.
        """

        target = self._normalize_id(target_id)

        nodes = list(self.routing_table.values())

        nodes.sort(
            key=lambda node: target ^ self._normalize_id(node["node_id"])
        )

        return nodes[:count]

    def get_nodes(self):
        """
        Return all nodes currently in the routing table.
        """

        return list(self.routing_table.values())

    def __len__(self):
        return len(self.routing_table)