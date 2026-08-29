import time

from meshweaver.node import MeshNode


def main():

    node = MeshNode(port=9001)

    peer_id = "test-peer"

    # Add a test peer
    node.add_peer(
        peer_id,
        "127.0.0.1",
        9002
    )

    # Simulate an old heartbeat
    node.peer_last_seen[peer_id] = time.time() - 20

    print("\n--- Before health check ---")
    print(node.get_peers())

    print("\n--- Checking peer health ---")

    node.check_peer_health(timeout=10)

    print("\n--- After health check ---")
    print(node.get_peers())


if __name__ == "__main__":
    main()