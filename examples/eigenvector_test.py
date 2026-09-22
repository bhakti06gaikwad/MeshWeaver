from meshweaver.eigenvector import eigenvector_centrality


def main():
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B", "D"],
        "D": ["C"]
    }

    results = eigenvector_centrality(graph)

    print("--- Eigenvector Centrality ---")

    for node, score in results.items():
        print(f"Node {node}: {score:.4f}")


if __name__ == "__main__":
    main()
