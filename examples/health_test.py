from meshweaver.health import (
    calculate_health_score,
    get_health_status
)


def main():
    score = calculate_health_score(
        cpu_percent=25,
        memory_percent=40,
        is_online=True
    )

    status = get_health_status(score)

    print("--- Node Health Test ---")
    print(f"Health Score: {score}/100")
    print(f"Health Status: {status}")

    offline_score = calculate_health_score(
        cpu_percent=20,
        memory_percent=30,
        is_online=False
    )

    print("\nOffline Node Score:", offline_score)


if __name__ == "__main__":
    main()