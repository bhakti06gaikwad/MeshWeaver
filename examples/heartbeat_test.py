import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    print("\n--- Node 1 sends heartbeat ---")

    await node1.heartbeat(
        "127.0.0.1",
        9002
    )

    await asyncio.sleep(2)

    print("\n--- Node 1 heartbeat status ---")

    print(node1.peer_last_seen)

    print(
        f"Node 1 received "
        f"{len(node1.peer_last_seen)} heartbeat response(s)"
    )

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())
    