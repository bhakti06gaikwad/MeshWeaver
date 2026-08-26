import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    print("\n--- Sending task ---")

    task = {
        "task_id": "task-001",
        "operation": "add",
        "numbers": [10, 20, 30],
    }

    node1.send_message(
        {
            "type": "TASK",
            "sender": node1.node_id,
            "task": task,
        },
        "127.0.0.1",
        9002
    )

    await asyncio.sleep(2)

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())