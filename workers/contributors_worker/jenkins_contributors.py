from github import Github
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from data_redis import make_name,store


# ----------- Authentication ---------- #
# input authentication token string
token = 'ec000918e9b6f3685895d45ed1d682f180e6f45d'  # TODO: DELETE THIS LATER !!!!
# token = 'token'
# ------------------------------------- #


def make_output(con):
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


def do_contributors(repo_name, time):
    try:
        repo = g.get_repo(repo_name)
        con = repo.get_contributors()
        store(make_name(repo_name, time, "contributors"), make_output(con))
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
    do_contributors(repo, time)
