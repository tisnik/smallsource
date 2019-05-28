from flask import Flask
app = Flask(__name__)

from flask import render_template

from datastore import db_source as db
from datastore import db_packages as pk


database = db.SqlalchemyDatabase('sqlite:///dbfile.db')

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/search')
def search():
    return render_template('Search.html')

@app.route('/eco')
def ecosystem():
    list = database.restore_all('Ecosystem')
    return render_template('Ecosystem.html', list = list)

@app.route('/<eco>/pac')
def packages(eco):
    link = eco.split("_")
    link = " ".join(link)
    link = link.title()
    packages = database.restore_from_master(link, 'Ecosystem')
    return render_template('Packages.html', name = link, list = packages)

@app.route('/<pac>/ver')
def versions(pac):
    package = pac.title()
    versions = database.restore_from_master(package, 'Packages')
    return render_template('Versions.html', name = package, list = versions)