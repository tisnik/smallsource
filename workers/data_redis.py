import redis
import json

r = redis.StrictRedis()


def make_name(repository,  worker_name, time, ip_address):
    """ Compose a string to serve as ID for Json string stored in Redis database """
    output = str(repository) + str(worker_name) + str(time) + str(ip_address)

    return output.replace(" ", "")


def store(name, data):
    """ Store Json sting into Redis database """
    r.execute_command('JSON.SET', name, '.', json.dumps(data))



def retrieve(name):
    """ Get data from Redis database in form of dictionary """
    data = r.execute_command('JSON.GET', name)
    if data is not None:
        reply = json.loads(data)
        return reply



