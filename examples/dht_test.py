import asyncio

from meshweaver.node import MeshNode


async def main():

    node1 = MeshNode(port=9001)
    node2 = MeshNode(port=9002)
    node3 = MeshNode(port=9003)
    node4 = MeshNode(port=9004)

    await node1.start()
    await node2.start()
    await node3.start()
    await node4.start()

    print("\nAdding nodes to Node 1 DHT...\n")

    node1.add_dht_peer(
        node2.node_id,
        node2.host,
        node2.port
    )

    node1.add_dht_peer(
        node3.node_id,
        node3.host,
        node3.port
    )

    node1.add_dht_peer(
        node4.node_id,
        node4.host,
        node4.port
    )

    print("\nDHT routing table:")

    for node in node1.dht.get_nodes():
        print(
            f"Node: {node['node_id']} "
            f"| {node['host']}:{node['port']} "
            f"| distance: {node['distance']}"
        )

    print("\nTotal DHT nodes:", len(node1.dht))

    print("\nFinding closest peers to Node 2...")

    closest = node1.find_closest_peers(
        node2.node_id,
        count=2
    )

    for peer in closest:
        print(
            f"Closest: "
            f"{peer['node_id']} "
            f"-> {peer['host']}:{peer['port']}"
        )

    node1.stop()
    node2.stop()
    node3.stop()
    node4.stop()


if __name__ == "__main__":
    asyncio.run(main())