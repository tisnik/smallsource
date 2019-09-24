import json
import requests

# ----------- Authentication ---------- #
# username = 'username'
# token = 'token'
# ------------------------------------- #


# prints out languages and number of bytes of code written in them
def get_data(response):
    data = json.loads(response.text)
    for i in data:
        print(f"{i} : {data[i]} bytes")


# ---------------------------- MAIN --------------------------- #
# worker is called by this function
# function takes repository name ['user/repository'] and prints out languages used and their size in bytes
def do_languages(repo):
    url = 'https://api.github.com/repos/' + repo + '/languages'
    gh_session = requests.Session()
    # ----------- Authentication ---------- #
    # gh_session.auth = (username, token)
    # ------------------------------------- #
    response = gh_session.get(url)
    if response.status_code == 200:
        get_data(response)
    else:
        raise Exception(f"Response status code : {response.status_code}")
do_languages("electron/electron")

# ------------------------------------------------------------- #
