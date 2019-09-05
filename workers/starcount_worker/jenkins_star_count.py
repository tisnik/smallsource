from github import Github
import os
import redis
import json

r = redis.StrictRedis()


# ----------- Authentication ---------- #
# input authentication token string
token = 'ec000918e9b6f3685895d45ed1d682f180e6f45d'  # TODO: DELETE THIS LATER !!!!
# token = 'token'
# ------------------------------------- #
try:
    g = Github(login_or_token=token, per_page=100)
except:
    print("Running without authentication")
    g = Github(per_page=100)


def make_name(repository,time):
    output = repository + "_starcount_" + time
    return output


def make_output(starcount):
    output = {
        'starcount': starcount
    }
    return output

def store_redis(name,data):
    #r.execute_command('JSON.SET', name, '.', json.dumps(data))
    print(name)
    print(json.dumps(data))

import os
import sys

p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

from smallsource.message-broker.data_redis import store

store("hello","{'hello':'nope'}")



# ---------------------------- MAIN --------------------------- #
# worker is called by this function
# function takes repository name ['user/repository'] and prints out star count of given repository
def do_star_count(repo,time):
    try:
        repo_name = repo
        repository = g.get_repo(repo)
        starcount = repository.stargazers_count
        store_redis(make_name(repo_name,time),make_output(starcount))
    except Exception as error:
        print(f"Error : {error}")
        exit(1)


if __name__ == '__main__':
    #repo = os.getenv('REPOSITORY')
    #time = os.getenv('TIME_OF_BUILD')
    do_star_count("tisnik/smallsource","sometime")
# ------------------------------------------------------------- #


