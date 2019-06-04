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
session = database.Session()


def MakeUrl(url):
    new_url = url.split("_")
    new_url = " ".join(new_url)
    new_url = new_url.title()
    return new_url


class Search(FlaskForm):
    name = wtf.StringField('Name', validators=[wtf.validators.DataRequired()])


@app.route('/')
def main():
    return render_template('Main.html')


@app.route('/search', methods=('GET', 'POST'))
def ssearch():
    add_form = Search()
    if add_form.validate_on_submit():
        name = add_form.name.data
        if database.restore_from_table(name, 'Ecosystem') is not None:
            return flask.redirect('/{}'.format(name))
        elif database.restore_from_table(name, 'Packages') is not None:
            eco = database.restore_from_table(name, 'Packages')
            url = MakeUrl(eco.package.name)
            return flask.redirect('/{}/{}'.format(url, name))
        else:
            return render_template('Error.html')
    return render_template('Search.html', form=add_form)



@app.route('/eco')
def ecosystem():
    restored = database.restore_all('Ecosystem')
    for i in restored:
        url = MakeUrl(i.name)
        i.link = url
    return render_template('Ecosystem.html', list=restored)


@app.route('/<eco>')
def packages(eco):
    url = MakeUrl(eco)
    packages = database.restore_from_master(url, 'Ecosystem')
    for i in packages:
        i.url = i.name.title()
    return render_template('Packages.html', name=url, list=packages)


@app.route('/<eco>/<pac>')
def versions(eco, pac):
    package = pac.title()
    versions = database.restore_from_master(package, 'Packages')
    return render_template('Versions.html', name=package, list=versions, eco=eco)
