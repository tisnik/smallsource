import redis
import json

r = redis.StrictRedis()


def make_name(repository,time,worker_name):
    output = repository + worker_name + time
    return output


def store(name,data):
    #r.execute_command('JSON.SET', name, '.', json.dumps(data))
    print(json.dumps(data))



def retrieve(name):
    reply = json.loads(r.execute_command('JSON.GET', name))
    print(reply)







    # TODO : To work with each worker we need to pass parameters into it with data about who ran it(ip address or something) and maybe timestamp