import redis
import json

r = redis.StrictRedis()


def make_name(repository, time, worker_name, ip_address):
    """ Compose a string to serve as ID for Json string stored in Redis """
    output = str(repository) + str(worker_name) + str(time) + str(ip_address)
    print(output)
    return output


def store(name, data):
    """ Store Json sting into Redis """
    #r.execute_command('JSON.SET', name, '.', json.dumps(data))
    print(json.dumps(data))


def retrieve(name):
    """ Get data from Redis in form of dictionary """
    reply = json.loads(r.execute_command('JSON.GET', name))
    print(reply)





