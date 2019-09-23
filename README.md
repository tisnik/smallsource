# smallsource
Source code analytics platform

## Installation

The system requires several tools to be installed:
* redis
* rq (Redis Queue)
* sqlite3

see requirements [here](requirements.txt).

### Redis
Redis database is used to store outputs of workers in Json format. We use Redis module https://github.com/RedisJSON/RedisJSON . 

### rq (Redis Queue)
Run workers by "rq worker" plus names of queues.
Example :  rq worker repo_fetcher star_count languages contributors
### sqlite3

## Other documents

### System architecture
please see documentation [here](doc/architecture.md)

The overall architecture can be displayed [as a PNG raster image](doc/architecture.png)
or [as vector drawing](doc/architecture.svg)


### QA-related tools
please see documentation [here](qa/README.md)

### Various tools used along the project
please see documentation [here](tools/README.md)
