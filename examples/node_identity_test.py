import asyncio

from meshweaver.node import MeshNode


async def main():
    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    print("\nNode 1:")
    print(node1.get_metadata())

    print("\nNode 2:")
    print(node2.get_metadata())

    print("\nIDs are different:", node1.node_id != node2.node_id)

    node1.stop()
    node2.stop()


if __name__ == "__main__":
    asyncio.run(main())