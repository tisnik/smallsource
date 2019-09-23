# Workers

Implementation of all workers that are tied to the message queue.

Workers are implemented as python scripts.  Special worker, github_fetcher is a worker to be called
when cloning a repository is required for analysis. This worker should be automatically called with specific workers.
This functionality is not yet implemented. All workers are called as Jenkins jobs within a jenkins pipeline, please see documentation [here](workers/flask_jenkins/README.md).

## Implementation of new worker
To implement a new worker you need to implement it as python script, if needed within the script compose the output of worker into a Json format,
store it into Redis database with use of 'store' function from data_redis.py,  make a Jenkins job that runs
said script and add option of this new job into the Jenkinsfile of Smallsource_main. To implement it within flask as well,
add it into the list of worker choices, (in flask names can be capitalized, jenkins jobs should be all lowercase),
make a jinja template for displaying of the output and if needed also worker_table template. 
