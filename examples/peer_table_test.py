import asyncio

from meshweaver.node import MeshNode


async def main():
    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)
    node3 = MeshNode(port=9003)

    await node1.start()
    await node2.start()
    await node3.start()

    print("\nAdding peers...")

    node1.add_peer(
        node2.node_id,
        node2.host,
        node2.port
    )

    node1.add_peer(
        node3.node_id,
        node3.host,
        node3.port
    )

    print("\nNode 1 peer table:")

    for peer in node1.get_peers():
        print(peer)

    print("\nPeer count:", len(node1.get_peers()))

    print("\nNode 1 metadata:")
    print(node1.get_metadata())

    print("\nRemoving Node 3...")

    node1.remove_peer(node3.node_id)

    print("Peer count after removal:", len(node1.get_peers()))

    node1.stop()
    node2.stop()
    node3.stop()


if __name__ == "__main__":
    asyncio.run(main())