from collections import deque


def closeness_centrality(graph):
    """
    Calculate closeness centrality for each node.
    """

    centrality = {}

    for source in graph:
        distances = {node: -1 for node in graph}
        distances[source] = 0

        queue = deque([source])

        while queue:
            current = queue.popleft()

            for neighbor in graph[current]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        reachable_nodes = [
            distance for distance in distances.values()
            if distance > 0
        ]

        if reachable_nodes:
            total_distance = sum(reachable_nodes)
            centrality[source] = (
                len(reachable_nodes) / total_distance
            )
        else:
            centrality[source] = 0.0

    return centrality