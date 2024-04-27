class AsyncTaskBase:
    """
    A single task that can be done async.
    """
    pass


class MainTaskBase:
    """
    A single (hopefully) small task to be done on the main thread once a parent AsyncTask has completed
    """
    pass


class AsyncGroup:
    """
    A group of AsyncTasks with prerequisites. Can be queried for the percentage of the tasks completed.
    """
    pass


class AsyncTaskRunner:
    """
    There is a task runner per thread which repeated picks up tasks from a queue within the AsyncLoader.
    This in sures that the threads which are all daemon's don't kill themselves unless the AsyncLoader tells it too.
    """


class AsyncLoader:
    """
    The loader held by a Lux Window and will dish out AsyncTasks to at least one secondary thread.
    All threads are daemons.
    """
    pass