from github import Github

# ----------- Authentication ---------- #
# input authentication token string
# token = 'ec000918e9b6f3685895d45ed1d682f180e6f45d'  # TODO: DELETE THIS LATER !!!!
# token = 'token'
# ------------------------------------- #
try:
    g = Github(login_or_token=token, per_page=100)
except:
    print("Running without authentication")
    g = Github(per_page=100)


# ---------------------------- MAIN --------------------------- #
# worker is called by this function
# function takes repository name ['user/repository'] and prints out star count of given repository
def do_star_count(repo):
    try:
        repo = g.get_repo(repo)
        print(repo.stargazers_count)
    except Exception as error:
        print(f"Error : {error}")
        exit(1)
# ------------------------------------------------------------- #


