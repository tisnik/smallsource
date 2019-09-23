import jenkins
import json
import jenkinsapi
import requests
from datetime import datetime
from time import sleep


username = 'tester'
password = 'tester'
jenkins_url = 'http://localhost:8080'
main_pipeline_name = "Smallsource_main"

# these two are input from within UI. now are here only for testing
# ================== testing ================= #
list_of_workers = "starcount,languages"
repo_name = "tisnik/smallsource"
ip_address = ""
# ============================================ #


def get_server_instance():
    server = jenkins.Jenkins(jenkins_url, username=username, password=password)
    return server


 # NOT IMPORTANT
def running(server):
    print(server.get_running_builds())


# gives information about one particular build of a job specified by build_number
def one_job_info(job_name, build_number):
    """ Get information in form of Json string about one particular build of a job specified by build_number """
    url = jenkins_url + "/job/" + job_name + "/" + str(build_number) + "/wfapi/describe"
    auth = (username, password)
    hope = requests.get(url,auth=auth)
    return hope.json()


# gives complete information about every build of the job and job in general
def info_job(server):
    job = server.get_job_info(main_pipeline_name)
    return job


# gives complete information about build but not downstream or upstream
def info_build(server):
    build = server.get_build_info(main_pipeline_name, 70)
    return build


# print out Json so its easier to read :)
def print_dict(my_dict):
    print(json.dumps(my_dict, indent=4))




def build_main(server, list_of_workers, repo_name, ip_address):
    """ Trigger build of main pipeline in jenkins with parameters """
    time = datetime.utcnow()
    build_id = server.build_job(main_pipeline_name, {'repo': repo_name, 'workers_list': list_of_workers,
                                                     'time_of_trigger': time, "ip_address": ip_address})
    redis_names = []
    workers = list_of_workers.split(",")
    for i in workers:
        name = (repo_name+i+str(time)+str(ip_address)).replace(" ", "")
        redis_names.append(name)

    return build_id, redis_names


# returns build to get info from
def get_one_build(job_name, build_number):
    build = jenkinsapi.api.get_build(jenkins_url, job_name, build_number, username, password)
    return build



 # NOT IMPORTANT
# prints out status of current build
def build_status(build):
    return build.is_good()


def get_build_number(server, build_q_id):
    """ Get build number from build queue, it takes a while for queue to update and contain a built number """
    x = True
    while x:
        item = server.get_queue_item(build_q_id)
        try:
            sleep(1)
            build_number = item["executable"]["number"]
            x = False
        except:
            pass
    return build_number


def end_status(build_number):
    """ Print end status of all executed builds in pipeline """
    info = one_job_info(main_pipeline_name, build_number)
    for x in info["stages"]:
        print(x["name"] + " : " + x["status"])
    print("Pipeline status : " + info["status"])


if __name__ == '__main__':
    build_id, redis_names = build_main(get_server_instance(), list_of_workers, repo_name, ip_address)
    build_number = get_build_number(get_server_instance(), build_id)
    build = get_one_build(main_pipeline_name, build_number)
    print(build.get_params())
    while build.is_running():
        sleep(2)
    end_status(build_number)



# TODO: vypisat info o vsetkych buildoch co boli vramci pipeliny a ked nejaky failol tak namiesto vysledku
#  vypisat console output
# TODO: fixnut ze pise "is no good" ajked je build successful
