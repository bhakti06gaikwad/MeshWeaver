import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    # Simulate gossip information about Node 2.
    node1.peer_metadata[node2.node_id] = {
        "node_id": node2.node_id,
        "host": node2.host,
        "port": node2.port,
        "resources": {
            "cpu_percent": 10,
            "memory_percent": 20,
        },
    }

    print("\n--- Routing Task ---")

    task = {
        "task_id": "task-001",
        "operation": "demo",
        "data": "Hello MeshWeaver",
    }

    await node1.route_task(task)

    await asyncio.sleep(2)

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())