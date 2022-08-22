# SuperFastPython.com
# example of getting results for tasks as they are completed
from time import sleep
from random import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# custom task that will sleep for a variable amount of time
def task(value):
    # sleep for less than a second
    sleep(value)
    return f"Task= {value:.2f}"


# start the thread pool
with ThreadPoolExecutor(10) as executor:
    # submit tasks and collect futures
    futures = [executor.submit(task, i) for i in range(10)]
    # process task results as they are available
    futures.append(executor.submit(task, 12))
    # print(len(list(as_completed(futures,6))))
    finished_fs = set()
    buffer_size = 5
    while len(finished_fs) < buffer_size:
        for future in futures:
            # retrieve the result

            if future.done():
                finished_fs.add(future)
    print([finished_f.result() for finished_f in finished_fs])
