from flask import Flask
import flask

from flask import render_template

from flask_wtf import FlaskForm
import wtforms as wtf


from datastore import db_source as db

SECRET_KEY = 'IRrno6DzVXL5vsHhB66p1CBwawYDn2'

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

database = db.SqlalchemyDatabase('sqlite:///dbfile.db')


class Search(FlaskForm):
    name = wtf.StringField("Name", validators=[wtf.validators.DataRequired()])
    table = wtf.RadioField("Table", choices=[('eco', 'Ecosystem'), ('pac', 'Package')])


@app.route('/')
def main():
    return render_template('Main.html')


@app.route('/search', methods=('GET', "POST"))
def search():
    add_form = Search()
    if add_form.validate_on_submit():
        link = add_form.name.data
        table = add_form.table.data
        if table == 'eco':
            return flask.redirect('/{}/pac'.format(link))
        elif table == 'pac':
            return flask.redirect('/{}/ver'.format(link))
    return render_template('Search.html', form=add_form)


@app.route('/eco')
def ecosystem():
    list = database.restore_all('Ecosystem')
    return render_template('Ecosystem.html', list=list)


@app.route('/<eco>/pac', methods=('GET', 'POST'))
def packages(eco):
    link = eco.split("_")
    link = " ".join(link)
    link = link.title()
    packages = database.restore_from_master(link, 'Ecosystem')
    return render_template('Packages.html', name=link, list=packages)


@app.route('/<pac>/ver')
def versions(pac):
    package = pac.title()
    versions = database.restore_from_master(package, 'Packages')
    return render_template('Versions.html', name=package, list=versions)
