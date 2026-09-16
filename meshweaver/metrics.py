import threading
import time


class TaskMetrics:
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.tasks = []
        self.lock = threading.Lock()

    def record_task(
        self,
        task_id,
        node_id,
        status,
        duration=0,
        rerouted=False,
        message=""
    ):
        task = {
            "task_id": task_id,
            "node_id": node_id,
            "status": status,
            "duration": round(duration, 4),
            "rerouted": rerouted,
            "message": message,
            "timestamp": time.time()
        }

        with self.lock:
            self.tasks.append(task)

            if len(self.tasks) > self.max_history:
                self.tasks.pop(0)

    def get_history(self):
        with self.lock:
            return list(self.tasks)

    def get_summary(self):
        with self.lock:
            total = len(self.tasks)
            completed = sum(
                t["status"] == "COMPLETED"
                for t in self.tasks
            )
            failed = sum(
                t["status"] == "FAILED"
                for t in self.tasks
            )
            rerouted = sum(
                t["rerouted"]
                for t in self.tasks
            )

            durations = [
                t["duration"]
                for t in self.tasks
                if t["duration"] > 0
            ]

            average = (
                sum(durations) / len(durations)
                if durations else 0
            )

            success_rate = (
                (completed / total) * 100
                if total else 0
            )

            return {
                "total": total,
                "completed": completed,
                "failed": failed,
                "rerouted": rerouted,
                "average_duration": round(average, 4),
                "success_rate": round(success_rate, 2)
            }