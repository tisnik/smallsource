from github import Github
import os

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


# ---------------------------- MAIN --------------------------- #
# worker is called by this function
# function takes repository name ['user/repository'] and prints out languages used and their size in bytes
def do_languages(repo):
    try:
        repo = g.get_repo(repo)
        print(repo.get_languages())
    except Exception as e:
        print(f"Error : {e}")
        exit(1)


repo = os.getenv('REPOSITORY')
do_languages(repo)
# ------------------------------------------------------------- #