import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    # Add Node 2 as a peer
    node1.add_peer(
        node2.node_id,
        node2.host,
        node2.port
    )

    # Give Node 2 resource information
    node1.peer_metadata[node2.node_id] = {
        "node_id": node2.node_id,
        "host": node2.host,
        "port": node2.port,
        "resources": {
            "cpu_percent": 20,
            "memory_percent": 30,
        },
    }

    print("\n--- Node 2 is ONLINE ---")

    task = {
        "task_id": "reroute-001",
        "operation": "add",
        "numbers": [100, 200],
    }

    await node1.route_task(task)

    await asyncio.sleep(2)

    print("\n--- Stopping Node 2 ---")

    node2.stop()

    node1.peers[node2.node_id]["status"] = "offline"

    print("\n--- Node 2 is OFFLINE ---")

    result = node1.select_task_node()

    print("Selected node after Node 2 failure:")
    print(result)

    node1.stop()


if __name__ == "__main__":
    asyncio.run(main())