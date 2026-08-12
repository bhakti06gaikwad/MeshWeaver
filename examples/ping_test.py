import asyncio
from meshweaver.node import MeshNode

async def main():
    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)

    await node1.start()
    await node2.start()

    await asyncio.sleep(1)

    await node1.ping("127.0.0.1",9002)

    await asyncio.sleep(2)

    node1.stop()
    node1.stop()

if __name__ == "__main__":
    asyncio.run(main())