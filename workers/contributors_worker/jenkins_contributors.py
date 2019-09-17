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
token = 'ec000918e9b6f3685895d45ed1d682f180e6f45d'  # TODO: DELETE THIS LATER !!!!
# token = 'token'
# ------------------------------------- #


def make_output(con):
    """ Compose Json string that will be stored in Redis """
    output = {}
    count = 0
    for i in con:
        output[count] = {
            "login": i.login,
            "html_url": i.html_url,
            "contributions": i.contributions
        }
        count += 1
    return output


def do_contributors(repo_name, time, ip_address):
    """ Get contributors data and store them into redis as Json string """
    try:
        repo = g.get_repo(repo_name)
        con = repo.get_contributors()
        # make_name function composes ID for Json to be stored in redis
        store(make_name(repo_name, time, "contributors", ip_address), make_output(con))
    except Exception as e:
        print(f"Error : {e}")
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
    do_contributors(repo, time, ip_address)

