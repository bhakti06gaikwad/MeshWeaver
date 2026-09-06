from meshweaver.security import sign_message, verify_message


def main():
    message = {
        "type": "TASK",
        "sender": "node-1",
        "task": {
            "task_id": "secure-fail-001",
            "operation": "add",
            "numbers": [10, 20],
        },
    }

    print("--- Invalid Signature Security Test ---")

    # Create a valid signature
    signature = sign_message(message)

    print("Original message:")
    print(message)

    print("\nValid signature:")
    print(signature)

    # Verify original message
    valid = verify_message(message, signature)
    print("\nOriginal message valid:", valid)

    # Modify the task after signing
    message["task"]["numbers"] = [10, 100]

    tampered = verify_message(message, signature)
    print("Tampered message valid:", tampered)

    # Test completely fake signature
    fake_signature = "invalid-signature"

    fake = verify_message(message, fake_signature)
    print("Fake signature valid:", fake)


if __name__ == "__main__":
    main()
    