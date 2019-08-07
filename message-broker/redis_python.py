from redis import Redis
from rq import Queue

from workers.workers_controller.controller import call_workers

controller_queue = Queue(connection=Redis())

# ------------------ SCUFFED INPUT ------------------ #
list_of_workers = ["star_count","languages"]
repo = "walker76/stackoversight"
# --------------------------------------------------- #


result = controller_queue.enqueue(call_workers,list_of_workers,repo)
print(result)


'''
Run workers by "rq worker" plus names of queues 
example :  rq worker repo_fetcher star_count languages contributors
'''


