import psutil


class ResourceMonitor:
    # Monitor CPU and memory usage of the current machine.

    @staticmethod
    def get_cpu_usage():
        """Return CPU usage percentage."""

        return psutil.cpu_percent(interval=0.1)

    @staticmethod
    def get_memory_usage():
        """Return memory usage percentage."""

        return psutil.virtual_memory().percent

    @classmethod
    def get_resources(cls):
        """Return current system resource information."""

        return {
            "cpu_percent": cls.get_cpu_usage(),
            "memory_percent": cls.get_memory_usage(),
        }