from redis import Redis
from rq import Queue

from test_worker import do_work


q = Queue("test", connection=Redis())

result = q.enqueue(do_work)
print(result)
