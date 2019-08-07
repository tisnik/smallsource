from redis import Redis
from rq import Queue
import os
from workers.workers_controller.controller import call_workers

controller_queue = Queue(connection=Redis())

# ----------------- ENVIRONMENT VARIABLES ------------------- #
# list_of_workers = ["star_count","languages","contributors","repo_fetcher"]
# repo = "walker76/stackoversight"
# ----------------------------------------------------------- #


key = 'repo'
repo = os.getenv(key)
key = 'list_of_workers'
list_of_workers = list(os.getenv(key).split(','))

# ------------------ SCUFFED INPUT ------------------ #
#list_of_workers = ["star_count","languages","contributors","repo_fetcher"]
# format for repository is [user/repository]
#repo = "electron/electron"
# --------------------------------------------------- #


if repo is None:
    raise Exception("Error : Environment variable 'repo' missing !")
    exit(1)
elif list_of_workers is None:
    raise Exception("Error : Environment variable 'list_of_workers' missing !")
    exit(1)
else:
    result = controller_queue.enqueue(call_workers, list_of_workers, repo)
    print(result)


'''
Run workers by "rq worker" plus names of queues 
example :  rq worker repo_fetcher star_count languages contributors
'''


