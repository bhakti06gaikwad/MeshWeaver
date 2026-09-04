import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    node1.add_peer(
        node2.node_id,
        node2.host,
        node2.port
    )

    task = {
        "task_id": "secure-001",
        "operation": "add",
        "numbers": [10, 20, 30],
    }

    print("\n--- Sending signed task ---")

    await node1.route_task(task)

    await asyncio.sleep(2)

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())