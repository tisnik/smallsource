import re
from os import path, makedirs
from os.path import isdir, dirname
from git import Repo, InvalidGitRepositoryError, GitCommandError
from .errors.UserInputError import UserInputError
from .config import config

from workers import __file__ as base_path

# Base directory for all cloned repositories is "[main module root directory]/repos/".
#clone_root_dir = path.join(dirname(base_path), "repos")

#temporary path for testing
clone_root_dir = path.join("/home/samuel_RH/RH_projects/test_smallsource","repos")


# TODO add info about repos
class RepoInfo:  # TODO: Add docstrings.
    def __init__(self, url, server, user, name):
        self.url = url
        self.server = server
        self.user = user
        self.name = name

        self.dir = path.join(clone_root_dir, server, user, name)
        self.hash = None


def _clone_repo(repo_url):
    """
    Clones the specified repository into a special internal directory and
    returns the directory path of the cloned repository.

    Arguments:
        repo_url {string} -- URL of the repository to clone.

    Returns:
        ClonedRepo -- Information about the cloned repository.
    """

    # Make sure the base clone dir exists.
    makedirs(clone_root_dir, exist_ok=True)

    # NOTE: Only standard GitHub and GitLab are currently properly supported.
    match = re.fullmatch(
        r"^(?:https?://)?(?:[\w\-\.]*\.)?([\w\-]+)\.\w{1,10}/([\w\-]+)/([\w\-]+)(?:/?\.git)?/?$", repo_url)
    # re.fullmatch returns None if there is no match so following might be redundant
    if not match:
        return None

    info = RepoInfo(repo_url, match[1], match[2], match[3])

    try:
        # If repo dir already exists, pull it.
        if isdir(info.dir):
            repo = Repo(info.dir)
            repo.remotes.origin.pull()

        # If the repo hasn't been cloned yet, clone it.
        else:
            repo = Repo.clone_from(info.url, info.dir)
        # Get HEAD's hash and store it in repo info.
        info.hash = repo.head.object.hexsha

    except InvalidGitRepositoryError:
        return None

    except GitCommandError:
        return None

    return info


def _clone_github_short(short_path):  # TODO: Add docstring.
    if re.fullmatch(r"^[\w\-]+/[\w\-]+(?:\.git)?$", short_path):
        return _clone_repo("https://github.com/" + short_path)
    else:
        return None


def get_repo_or_dir(repo):
    """
    Attempts to process the given repository path in many different ways.
    If all of them fail, an error message will be printed and
    the script with exit with a non-zero exit code.
    If one of them succeeds, local path of the repository will be returned.

    Arguments:
        repo {string} -- Path to the repository or local directory.

    Returns:
        string -- Local path to the repository's directory.
    """

    # TODO: This option should probably be removed in the future.
    # It is more confusing than it is practical now.

    # Path of a previously cloned repository: "[server]/[user]/[repo name]"
    repo_dir_by_name = path.join(clone_root_dir, repo)
    if re.fullmatch(r"^[\w\-]+/[\w\-]+/[\w\-]+$", repo) and isdir(repo_dir_by_name):
        return repo_dir_by_name

    # Shorthand for GitHub URLs: "[repository owner]/[repository name]"
    repo_info = _clone_github_short(repo)
    if repo_info:
        return repo_info.dir

    # Local directory path
    if isdir(repo):
        if config.allow_local_access:
            return repo
        else:
            raise UserInputError(
                f"Access to local directory denied: \"{repo}\"")

    # Full remote repository URL
    repo_info = _clone_repo(repo)
    if repo_info:
        return repo_info.dir

    raise UserInputError(f"Invalid repository path: \"{repo}\"")


def get_repo_info(repo):  # TODO: Add docstring.
    return _clone_github_short(repo) or _clone_repo(repo)




# ---------------------- Main function ------------------------ #

# function to call as worker
def do_repo_cloner(repo):
    path_to_repo = get_repo_or_dir(repo)
    print(path_to_repo)


# for testing
# do_repo_cloner("electron/electron")
# ------------------------------------------------------------- #
