import asyncio

from meshweaver.node import MeshNode


async def run_cli():

    node = MeshNode(port=9001)

    await node.start()

    print("\n==============================")
    print("      MeshWeaver CLI")
    print("==============================")

    while True:

        print("\n1. Show Node Metadata")
        print("2. Show Peers")
        print("3. Show Resources")
        print("4. Send Heartbeat")
        print("5. Send Task")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            print("\n--- Node Metadata ---")
            print(node.get_metadata())

        elif choice == "2":

            print("\n--- Known Peers ---")

            peers = node.get_peers()

            if not peers:
                print("No peers available")
            else:
                for peer in peers:
                    print(peer)

        elif choice == "3":

            print("\n--- System Resources ---")

            resources = node.get_resources()

            print(
                f"CPU usage: "
                f"{resources['cpu_percent']}%"
            )

            print(
                f"Memory usage: "
                f"{resources['memory_percent']}%"
            )

        elif choice == "4":

            host = input("Peer host: ").strip()
            port = int(input("Peer port: ").strip())

            await node.heartbeat(host, port)

        elif choice == "5":

            operation = input(
                "Operation (demo/add): "
            ).strip()

            if operation == "add":

                numbers_input = input(
                    "Enter numbers separated by spaces: "
                )

                numbers = [
                    int(number)
                    for number in numbers_input.split()
                ]

                task = {
                    "task_id": "cli-task",
                    "operation": "add",
                    "numbers": numbers,
                }

            else:

                data = input("Enter task data: ")

                task = {
                    "task_id": "cli-task",
                    "operation": "demo",
                    "data": data,
                }

            await node.route_task(task)

        elif choice == "6":

            print("\nStopping MeshWeaver...")

            node.stop()

            break

        else:

            print("Invalid choice. Please select 1-6.")


def main():
    asyncio.run(run_cli())


if __name__ == "__main__":
    main()