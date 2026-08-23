from meshweaver.monitor import ResourceMonitor
from meshweaver.node import MeshNode


def main():

    print("--- System Resources ---")

    resources = ResourceMonitor.get_resources()

    print(f"CPU usage: {resources['cpu_percent']}%")
    print(f"Memory usage: {resources['memory_percent']}%")

    print("\n--- Node Metadata ---")

    node = MeshNode(port=9001)

    print(node.get_metadata())


if __name__ == "__main__":
    main()