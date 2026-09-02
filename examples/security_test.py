from meshweaver.security import (
    sign_message,
    verify_message
)


def main():

    message = {
        "type": "TASK",
        "task_id": "security-001",
        "operation": "add",
        "numbers": [10, 20]
    }

    print("--- Security Test ---")

    signature = sign_message(message)

    print("Message:")
    print(message)

    print("\nSignature:")
    print(signature)

    valid = verify_message(
        message,
        signature
    )

    print("\nSignature valid:", valid)

    # Test tampering
    message["numbers"] = [10, 50]

    tampered = verify_message(
        message,
        signature
    )

    print(
        "Tampered message valid:",
        tampered
    )


if __name__ == "__main__":
    main()
    