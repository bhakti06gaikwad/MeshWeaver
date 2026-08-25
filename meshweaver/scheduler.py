class TaskScheduler:
    #Select the best node for executing a task.

    def __init__(self, node):
        self.node = node

    def select_node(self):
        """Select the node with the lowest combined CPU and memory usage."""

        candidates = []

        # Include known peer metadata
        for node_id, metadata in self.node.peer_metadata.items():
            resources = metadata.get("resources", {})

            cpu = resources.get("cpu_percent")
            memory = resources.get("memory_percent")

            if cpu is None or memory is None:
                continue

            score = cpu + memory

            candidates.append({
                "node_id": node_id,
                "host": metadata.get("host"),
                "port": metadata.get("port"),
                "cpu_percent": cpu,
                "memory_percent": memory,
                "score": score,
            })

        # Include the current node
        resources = self.node.get_resources()

        candidates.append({
            "node_id": self.node.node_id,
            "host": self.node.host,
            "port": self.node.port,
            "cpu_percent": resources["cpu_percent"],
            "memory_percent": resources["memory_percent"],
            "score": (
                resources["cpu_percent"]
                + resources["memory_percent"]
            ),
        })

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda node: node["score"]
        )