from flask import Flask, render_template, request , session , Response
from flask_wtf import FlaskForm
from wtforms import SubmitField
import os

from .jenkins_control import build_main,get_server_instance
from ..data_redis import retrieve
from jinja2 import Environment

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])

class AppInputForm(FlaskForm):

    submit = SubmitField('Start')
    result = SubmitField('View Results')


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/app', methods=['GET', 'POST'])
def application():

    session.pop('list_of_workers', None)
    session.pop('names', None)
    session.pop('last', None)

    form = AppInputForm()
    value = ''

    if request.method == 'POST':
        errors = []
        multiselect = request.form.getlist('mymultiselect')
        repo = request.form.get('repo_url')

        if not repo:
            errors.append('EmptyRepo')
            repo_ok = False
        else:
            value = repo
            repo_ok = True
        if not multiselect:
            errors.append('EmptySelect')
        elif repo_ok:
            list_of_workers = multiselect
            repo_name = repo
            # triggering jenkins part
            mystring = list_of_workers[0].lower()
            for i in range(len(list_of_workers) - 1):
                mystring = mystring + "," + list_of_workers[i + 1].lower()
            string_of_workers = mystring
            ip_address = request.remote_addr
            session['list_of_workers'] = list_of_workers
            # this function triggers build of jenkins pipeline Smallsource_main
            _, session['names'] = build_main(get_server_instance(), string_of_workers, repo_name, ip_address)

            return render_template('app.html', form=form,value=value, success=True)

        return render_template('app.html', form=form, errors=errors, value=value, success=False)

    return render_template('app.html', form=form, value=value,success=False)


def check_session():
    """ Check if session has essential data. If not, deny access."""
    if 'list_of_workers' in session:
        list_o_w = session['list_of_workers']
    else:
        raise Exception("Permisson denied")
    if 'names' in session:
        names = session['names']
    else:
        raise Exception("Permisson denied")

    return list_o_w, names


def compose_output(list_o_w, names):
    """ Compose output_data dictionary to be displayed in UI as workers results content """
    output_data = {}

    for i in range(len(names)):
        key = list_o_w[i].lower()
        output_data[key] = retrieve(names[i])

    return output_data


@app.route('/app/upload_success')
def upload_success():
    try:
        list_o_w, names = check_session()
    except Exception as e:
        return str(e)
    session.pop('last', None)
    output_data = compose_output(list_o_w, names)

    return render_template('upload_success.html', workers=list_o_w, output=output_data)



@app.route('/app/upload_success/update', methods=['POST'])
def update():
    try:
        list_o_w, names = check_session()
    except Exception as e:
        return str(e)

    output_data = compose_output(list_o_w, names)

    end_me = True

    if 'last' not in session:
        session['last'] = False

    for i in output_data.values():
        if i is None:
            end_me = False
            break

    if end_me:
        if session['last']:

            return Response('END')
        else:
            session['last'] = True
            return render_template('section.html', workers=list_o_w, output=output_data)
    else:
        return render_template('section.html', workers=list_o_w, output=output_data)


@app.route('/table/<name>',methods=['GET'])
def table(name):
    try:
        list_o_w, names = check_session()
    except Exception as e:
        return str(e)

    output_data = compose_output(list_o_w, names)
    data = output_data[name]
    return render_template("/worker_templates/"+name+"_table.html", data=data)

if __name__ == '__main__':
    app.run(port="5000")


# TODO : handle error cases with wrong repository names