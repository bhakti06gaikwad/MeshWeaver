def eigenvector_centrality(graph, iterations=100, tolerance=0.0001):
    """
    Calculate eigenvector centrality using the power iteration method.
    """

    nodes = list(graph.keys())

    if not nodes:
        return {}

    # Initial score for every node
    scores = {
        node: 1.0
        for node in nodes
    }

    for _ in range(iterations):
        new_scores = {
            node: 0.0
            for node in nodes
        }

        # Calculate new score
        for node in nodes:
            for neighbor in graph[node]:
                if neighbor in scores:
                    new_scores[node] += scores[neighbor]

        # Normalize scores
        magnitude = sum(
            value ** 2
            for value in new_scores.values()
        ) ** 0.5

        if magnitude == 0:
            return scores

        for node in nodes:
            new_scores[node] /= magnitude

        # Check convergence
        difference = sum(
            abs(new_scores[node] - scores[node])
            for node in nodes
        )

        scores = new_scores

        if difference < tolerance:
            break

    return scores