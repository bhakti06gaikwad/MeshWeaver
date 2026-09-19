from meshweaver.closeness import closeness_centrality


def main():
    graph = {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C"]
    }

    results = closeness_centrality(graph)

    print("--- Closeness Centrality ---")

    for node, score in results.items():
        print(f"Node {node}: {score:.2f}")


if __name__ == "__main__":
    main()