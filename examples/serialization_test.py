from meshweaver.serializer import serialize_task, execute_task


def calculate(a, b):
    return (a * b) + 10


def main():
    data = serialize_task(calculate, 5, 6)

    print("Task serialized successfully.")
    print(f"Serialized size: {len(data)} bytes")

    result = execute_task(data)

    print(f"Task result: {result}")


if __name__ == "__main__":
    main()