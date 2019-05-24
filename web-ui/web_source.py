from flask import Flask
app = Flask(__name__)

from flask import render_template

from datastore import db_source as db
from datastore import db_packages as pk


database = db.CreateDatebase()

y = [pk.Package('First Generation'), pk.Package('Second Generation')]
database.store(y)

x = database.restore_all('Ecosystem')

@app.route('/')
def main():
    return render_template('main.html', list = x)

