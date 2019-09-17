from redis import Redis
from rq import Queue
import os
from workers.workers_controller.controller import call_workers


controller_queue = Queue(connection=Redis())

# ----------------- ENVIRONMENT VARIABLES ------------------- #
# Example :
# list_of_workers = ["star_count","languages","contributors","repo_fetcher"]
# repo = "tisnik/smallsource"
# ----------------------------------------------------------- #

key = 'repo'
repo = os.getenv(key)
key = 'list_of_workers'
list_of_workers = list(os.getenv(key).split(','))

if repo is None:
    raise Exception("Error : Environment variable 'repo' missing !")

elif list_of_workers is None:
    raise Exception("Error : Environment variable 'list_of_workers' missing !")

else:
    result = controller_queue.enqueue(call_workers, list_of_workers, repo)
    print(result)


'''
Run workers by "rq worker" plus names of queues 
example :  rq worker repo_fetcher star_count languages contributors
'''
