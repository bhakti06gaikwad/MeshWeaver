from meshweaver.node import MeshNode


def main():

    node = MeshNode(port=9001)

    # Simulate information received through gossip
    node.peer_metadata = {
        "node-2": {
            "node_id": "node-2",
            "host": "127.0.0.1",
            "port": 9002,
            "resources": {
                "cpu_percent": 20,
                "memory_percent": 30,
            },
        },
        "node-3": {
            "node_id": "node-3",
            "host": "127.0.0.1",
            "port": 9003,
            "resources": {
                "cpu_percent": 70,
                "memory_percent": 60,
            },
        },
    }

    print("--- Task Scheduling ---")

    selected = node.select_task_node()

    print("\nSelected node:")

    if selected:
        print(selected)


if __name__ == "__main__":
    main()