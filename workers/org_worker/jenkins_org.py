from github import Github
import os


# ----------- Authentication ---------- #
# input authentication token string
token = 'ec000918e9b6f3685895d45ed1d682f180e6f45d'  # TODO: DELETE THIS LATER !!!!
# token = 'token'
# ------------------------------------- #
try:
    g = Github(login_or_token=token, per_page=100)
    print("Running with authentication")
except:
    print("Running without authentication")
    g = Github(per_page=100)


# ---------------------------- MAIN --------------------------- #
# worker is called by this function
# function takes repository name ['user/repository'] and prints out info about organization that repository belong to
def do_org(repo):
    try:
        repo = g.get_repo(repo)
        org = repo.organization
        if org is None:
            print("No organization.")
        else:
            print(f"Name : {org.name}")
            print(f"Email : {org.email}")
            print(f"Link : {org.html_url}")
            print(f"Company : {org.company}")
    except Exception as error:
        print(f"Error : {error}")
        exit(1)


repo = os.getenv('REPOSITORY')
do_org(repo)
# ------------------------------------------------------------- #
