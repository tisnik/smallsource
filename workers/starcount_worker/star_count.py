from github import Github


# ---------------------------- MAIN --------------------------- #
# worker is called by this function
# function takes repository name ['user/repository'] and prints out star count of given repository
def do_star_count(repo):
    g = Github()
    try:
        repo = g.get_repo(repo)
        print(repo.stargazers_count)
    except Exception as error:
        print(f"Error : {error}")
        exit(1)

# ------------------------------------------------------------- #


