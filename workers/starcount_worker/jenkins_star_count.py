from github import Github
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,parent_dir)

from data_redis import make_name,store


# ----------- Authentication ---------- #
# input authentication token string
# token = 'token'
# ------------------------------------- #


def make_output(starcount):
    """ Compose Json string that will be stored in Redis """
    output = {
        'starcount': starcount
    }
    return output


def do_star_count(repo_name, time, ip_address):
    """ Get star count of repository store it into redis as Json string """
    try:
        repository = g.get_repo(repo_name)
        starcount = repository.stargazers_count
        # make_name function composes ID for Json to be stored in redis
        store(make_name(repo_name, "starcount", time, ip_address),make_output(starcount))
    except Exception as error:
        print(f"Error : {error}")
        exit(1)


if __name__ == '__main__':
    try:
        g = Github(login_or_token=token, per_page=100)
        print("Running with authentication")
    except:
        print("Running without authentication")
        g = Github(per_page=100)

    repo = os.getenv('REPOSITORY')
    time = os.getenv('TIME_OF_BUILD')
    ip_address = os.getenv('IP_ADDRESS')
    do_star_count(repo, time, ip_address)


