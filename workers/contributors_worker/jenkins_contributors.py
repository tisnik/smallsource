from github import Github


# ----------- Authentication ---------- #
# input authentication token string instead of None
#token = 'ec000918e9b6f3685895d45ed1d682f180e6f45d'   # TODO: DELETE THIS LATER !!!!
token = None
# ------------------------------------- #

g = Github(login_or_token=token, per_page=100)


# ---------------------------- MAIN ----------------------------#
# worker is called by this function
# function takes repository name ['user/repository'] and prints out username, profile link and number of contributions,
# for all contributors
def do_contributors(repo):
    try:
        repo = g.get_repo(repo)
        con = repo.get_contributors()
        for i in con:
            print(i.login)
            print(i.html_url)
            print(i.contributions)
    except Exception as e:
        print(f"Error : {e}")
        exit(1)

do_contributors("PyGithub/PyGithub")
# --------------------------------------------------------------#
