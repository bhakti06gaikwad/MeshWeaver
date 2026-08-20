import asyncio

from meshweaver.node import MeshNode


async def main():

    # Existing node in the mesh
    node1 = MeshNode(port=9001)

    # New node trying to join
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    # Give the sockets time to start.
    await asyncio.sleep(1)

    print("\n--- Node 2 joining Node 1 ---")

    await node2.join_peer(
        "127.0.0.1",
        9001
    )

    # Give Node 1 time to respond.
    await asyncio.sleep(2)

    print("\n--- Node 2 peer table ---")

    for peer in node2.get_peers():
        print(peer)

    print(
        "\nNode 2 discovered:",
        len(node2.get_peers()),
        "peer(s)"
    )

    print("\n--- Node 1 peer table ---")

    for peer in node1.get_peers():
        print(peer)

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())