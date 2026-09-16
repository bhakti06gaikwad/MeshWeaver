import time


def calculate_health_score(
    cpu_percent,
    memory_percent,
    is_online,
    last_heartbeat=None
):
    """
    Calculate node health using real monitoring data.

    Score range: 0–100
    """

    if not is_online:
        return 0

    cpu_percent = max(0, min(100, cpu_percent))
    memory_percent = max(0, min(100, memory_percent))

    resource_score = (
        (100 - cpu_percent) * 0.4
        + (100 - memory_percent) * 0.4
    )

    heartbeat_score = 20

    if last_heartbeat is not None:
        elapsed = time.time() - last_heartbeat

        if elapsed > 30:
            heartbeat_score = 0
        elif elapsed > 10:
            heartbeat_score = 10

    score = resource_score + heartbeat_score

    return round(max(0, min(100, score)), 2)


def get_health_status(score):
    """Return a readable health status."""

    if score >= 80:
        return "HEALTHY"

    if score >= 50:
        return "WARNING"

    return "CRITICAL"