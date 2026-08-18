import cloudpickle


def serialize_task(function, *args, **kwargs):
    """Serialize a Python function and its arguments."""

    task = {
        "function": function,
        "args": args,
        "kwargs": kwargs,
    }

    return cloudpickle.dumps(task)


def deserialize_task(data):
    """Deserialize a task."""

    return cloudpickle.loads(data)


def execute_task(data):
    """Deserialize and execute a serialized task."""

    task = deserialize_task(data)

    function = task["function"]
    args = task["args"]
    kwargs = task["kwargs"]

    return function(*args, **kwargs)