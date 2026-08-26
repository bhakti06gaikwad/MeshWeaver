class TaskExecutor:
    #Execute tasks received by a MeshWeaver node.

    def execute(self, task):
        task_id = task.get("task_id")
        operation = task.get("operation")
        data = task.get("data")

        if operation == "demo":
            result = f"Task completed: {data}"

        elif operation == "add":
            numbers = task.get("numbers", [])
            result = sum(numbers)

        else:
            result = f"Unknown operation: {operation}"

        return {
            "task_id": task_id,
            "success": True,
            "result": result,
        }