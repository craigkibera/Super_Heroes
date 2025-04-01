from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero , Power, HeroPower

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        } for hero in heroes
    ]
    return jsonify(heroes_list)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [
            {
                "id": hp.id,
                "hero_id": hp.hero_id,
                "power_id": hp.power_id,
                "strength": hp.strength,
                "power": {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                }
            } for hp in hero.hero_powers
        ]
    }
    return jsonify(hero_data)
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [
        {
        "description": power.description,
        "id": power.id,
        "name": power.name
        } for power in powers
    ]
    return jsonify(powers_list)
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    power_data = {
        "description": power.description,
        "id": power.id,
        "name": power.name, 
    }
    return jsonify(power_data)
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    data = request.get_json()
    if 'name' in data:
        power.name = data['name']
    if 'description' in data:
        power.description = data['description']
    db.session.commit()
    return jsonify({
        "description": power.description,
        "id": power.id,
        "name": power.name, 
    })
@app.route('/hero-powers', methods=['POST'])
def create_hero_powers():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
    
    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    if not all([strength, hero_id, power_id]):
        return jsonify({"error": "Missing required fields (strength, hero_id, power_id)"}), 400


    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero:
        return jsonify({"error": f"Hero with ID {hero_id} not found"}), 404
    if not power:
        return jsonify({"error": f"Power with ID {power_id} not found"}), 404

    try:
        hero_power = HeroPower(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id,
        )
        db.session.add(hero_power)
        db.session.commit()

        return jsonify({
            "id": hero_power.id,
            "hero_id": hero_power.hero_id,
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
