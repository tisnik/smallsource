import requests
import json

# ----------- Authentication ---------- #
# username = 'username'
# token = 'token'
# ------------------------------------- #

# prints out info about users
def get_data(response):
    data = json.loads(response.text)
    for i in range(len(data)):
        print(data[i]["login"])
        print(data[i]["html_url"])
        print(data[i]["contributions"])

# ------------ FOR TESTING ONLY ! ------------ #
# prints out links for the current page, only here for testing, not in final product !!!
def print_links(response):
    links = response.links
    for x in links:
        print(x)
        for y in links[x]:
            print(y, ':', links[x][y])
# -------------------------------------------- #


# recursively calls functions and itself to print out info from all pages
def print_page(prev_resp,session):
    if "next" in prev_resp.links:
        curr_resp = session.get(prev_resp.links["next"]['url'])
        # ------- FOR TESTING ONLY ! ------- #
        # print_links(curr_resp)
        # ---------------------------------- #
        get_data(curr_resp)
        print_page(curr_resp,session)
    else:
        return


# main function for printing all info
def print_all_pages(response,session):
    get_data(response)
    print_page(response, session)


# ---------------------------- MAIN ----------------------------#
# worker is called by this function
# function takes repository name ['user/repository'] and prints out username, profile link and number of contributions,
# for all contributors
def do_contributors(repo):
    url = 'https://api.github.com/repos/' + repo + '/contributors?per_page=100'
    gh_session = requests.Session()
    # ----------- Authentication ---------- #
    # gh_session.auth = (username, token)
    # ------------------------------------- #
    response = gh_session.get(url)
    if response.status_code == 200:
        print_all_pages(response, gh_session)
    else:
        raise Exception(f"Response status code : {response.status_code}")
do_contributors("PyGithub/PyGithub")
# --------------------------------------------------------------#
