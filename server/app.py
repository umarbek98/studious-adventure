#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
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

@app.route('/heroes', methods = ['GET'])
def heroes():
    all_heroes = Hero.query.all()
    heroes_dict = [hero.to_dict() for hero in all_heroes]
    if request.method == 'GET':
        return make_response(jsonify(heroes_dict), 200)

@app.route('/heroes/<int:id>', methods = ['GET'])
def hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()

    if not hero:
        return make_response(jsonify({"error": "Hero not found"}))
    
    if request.method == 'GET':
        return make_response(jsonify(hero.to_dict()),200)
    

@app.route('/powers', methods = ['GET'])
def powers():
    all_powers = Power.query.all()
    powers_dict = [power.to_dict() for power in all_powers]

    if request.method == 'GET':
        return make_response(jsonify(powers_dict), 200)

@app.route('/powers/<int:id>', methods = ['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.filter(Power.id == id).first()

    if not power:
        return make_response(jsonify({"error": "Power not found"}))
    
    if request.method == 'GET':
        return make_response(jsonify(power.to_dict()))
    
    elif request.method == 'PATCH':
        data = request.get_json()
        
        if not power:
            return make_response(jsonify({"error": "Power not found"}))
        
        for field in data:
            setattr(power, field, data[field])
        if len(power.description) < 20:
            return make_response({"error": "Invalid input: length must be >=20"})
        else:
            db.session.add(power)
            db.session.commit()
            return make_response(jsonify(power.to_dict()), 200)

@app.route('/hero_powers', methods = ['GET', 'POST'])
def hero_powers():
    hp = HeroPower.query.all()
    hp_dict = [power.to_dict() for power in hp]

    if request.method == 'GET':
        return make_response(jsonify(hp_dict), 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_hp = HeroPower()

        for field in data:
            setattr(new_hp, field, data[field])
        if new_hp.strength != 'Strong' and new_hp.strength != 'Weak' and new_hp.strength != 'Average':
            return make_response(jsonify({"error": "Invalid input"}))
        else:
            db.session.add(new_hp)
            db.session.commit()
            return make_response(jsonify(new_hp.hero.to_dict()), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
