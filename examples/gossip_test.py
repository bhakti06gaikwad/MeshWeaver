import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    print("\n--- Node 1 sends gossip to Node 2 ---")

    node1.gossip_to_peer(
        "127.0.0.1",
        9002
    )

    await asyncio.sleep(2)

    print("\n--- Node 2 stored metadata ---")

    for node_id, metadata in node2.peer_metadata.items():
        print(f"Node ID: {node_id}")
        print(f"Metadata: {metadata}")

    print(
        "\nKnown metadata:",
        len(node2.peer_metadata)
    )

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())