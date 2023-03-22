#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes')
def heroes():
    return ''

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    return ''

@app.route('/powers')
def powers():
    return ''

@app.route('/powers/<int:id>')
def power_by_id(id):
    return ''

@app.route('/hero_powers')
def hero_powers():
    return ''


if __name__ == '__main__':
    app.run(port=5555, debug=True)
