## Jenkins

This project is implemented using jenkins jobs and jenkins pipeline.
Every worker has its own parameterized jenkins job. Jenkins pipeline called Smallsource_main is 
the main pipeline which consists of Jenkinsfile that controls which jobs(workers) will be build, based on parameters.
To trigger a pipeline build with parameters a Flask application is used.

## Flask
FLASK_APP is to be set as flaskfile.py . Flask application on route /app takes repository in format ' username/repository '.Error cases are not yet handled.




 