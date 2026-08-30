from meshweaver.node import MeshNode


def main():

    node = MeshNode(port=9001)

    # Simulate two peers
    node.add_peer(
        "offline-node",
        "127.0.0.1",
        9002
    )

    node.add_peer(
        "online-node",
        "127.0.0.1",
        9003
    )

    # Mark first node offline
    node.peers["offline-node"]["status"] = "offline"

    # Give scheduler resource information
    node.peer_metadata = {
        "offline-node": {
            "node_id": "offline-node",
            "host": "127.0.0.1",
            "port": 9002,
            "resources": {
                "cpu_percent": 10,
                "memory_percent": 20,
            },
        },

        "online-node": {
            "node_id": "online-node",
            "host": "127.0.0.1",
            "port": 9003,
            "resources": {
                "cpu_percent": 20,
                "memory_percent": 30,
            },
        },
    }

    print("\n--- Peer Status ---")

    for peer in node.get_peers():
        print(peer)

    print("\n--- Task Routing ---")

    task = {
        "task_id": "retry-001",
        "operation": "add",
        "numbers": [10, 20],
    }

    # Test scheduler first
    selected = node.select_task_node()

    print("\nSelected node:")
    print(selected)


if __name__ == "__main__":
    main()