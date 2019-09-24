#imports for Redis Queues
from redis import Redis
from rq import Queue

""" This script is for use of rq, as of now we are using Jenkins pipelines so this script is not being used. """

#imports for workers

from workers.starcount_worker.star_count import do_star_count
from workers.contributors_worker.contributors_worker import do_contributors
from workers.languages_worker.languages import do_languages
from workers.github_fetcher.repo_cloner import do_repo_cloner

 # --------------------- Worker calls --------------------- #

# Input will be a list of workers to be called and repo [user/repository]

def call_workers(list_of_workers,repo):
    repo_fetcher_queue = Queue("repo_fetcher",connection=Redis())
    star_count_queue = Queue("star_count",connection=Redis())
    contributors_queue = Queue("contributors",connection=Redis())
    languages_queue = Queue("languages", connection=Redis())

    # TODO : later change to (if " " in list)
    for i in list_of_workers:
        if i == "star_count":
            star_count = star_count_queue.enqueue(do_star_count,repo)
            print(star_count)
        elif i == "contributors":
            contributors = contributors_queue.enqueue(do_contributors, repo)
            print(contributors)
        elif i == "languages":
            languages = languages_queue.enqueue(do_languages,repo)
            print(languages)
        elif i == "repo_fetcher":
            repository = repo_fetcher_queue.enqueue(do_repo_cloner,repo)
            print(repository)
        else:
            raise Exception("Unknown worker requested !")
