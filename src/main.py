"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin 
from models import *
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# GET users
@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

# GET a single user
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user: return jsonify({"error":"user not found"}), 404
    if user:
        user = user.serialize()
        return jsonify(user), 200


# GET people/characters
@app.route('/characters', methods=['GET'])
def get_characters():

    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))

    return jsonify(characters), 200

# GET a single character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character: return jsonify({"error":"character not found"}), 404
    if character:
        character = character.serialize()
        return jsonify(character), 200

# GET planets
@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets), 200

# GET a single planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet: return jsonify({"error": "planet not found"}), 404
    if planet:
        planet = planet.serialize()
        return jsonify(planet), 200

#POST a new user
@app.route('/users', methods=['POST'])
def add_new_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not email: return jsonify({"error":"email is required!"}), 400
    if not password: return jsonify({"error":"please enter a password"}), 400

    newUser = User()
    newUser.first_name = first_name
    newUser.last_name = last_name
    newUser.email = email
    newUser.password = password
    newUser.save()

    return jsonify(newUser.serialize()), 201

# POST a new planet
@app.route('/planets', methods=['POST'])
def add_new_planet():
    name = request.json.get('name')
    rotation_period = request.json.get('rotation_period')
    orbital_period = request.json.get('orbital_period')
    diameter = request.json.get('diameter')
    climate = request.json.get('climate')
    gravity = request.json.get('gravity')
    terrain = request.json.get('terrain')
    surface_water = request.json.get('surface_water')
    population = request.json.get('population')

    if not name: return jsonify({"error":"name is required"}), 400

    newPlanet = Planet()
    newPlanet.name = name
    newPlanet.rotation_period = rotation_period
    newPlanet.orbital_period = orbital_period
    newPlanet.diameter = diameter
    newPlanet.climate = climate
    newPlanet.gravity = gravity
    newPlanet.terrain = terrain
    newPlanet.surface_water = surface_water
    newPlanet.population = population
    newPlanet.save()

    return jsonify(newPlanet.serialize()), 201

#POST a new character
@app.route('/characters', methods=['POST'])
def add_new_character():
    name = request.json.get('name')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    eye_color = request.json.get('eye_color')
    birth_year = request.json.get('birth_year')
    gender = request.json.get('gender')

    if not name: return jsonify({"error":"name is required"}), 400

    newCharacter = Character()
    newCharacter.name = name
    newCharacter.height = height
    newCharacter.mass = mass
    newCharacter.hair_color = hair_color
    newCharacter.skin_color = skin_color
    newCharacter.eye_color = eye_color
    newCharacter.birth_year = birth_year
    newCharacter.gender = gender
    newCharacter.save()

    return jsonify(newCharacter.serialize()), 201

#GET ALL FAVORITES FROM A SPECIFIC USER
@app.route('/users/<int:id>/favorites')
def get_favorites_user(id):
    user=User.query.get(id)
    return jsonify(user.serialize_with_favorites()),200

#POST a character to favorites
@app.route('/users/<int:id>/favorites/characters/<int:character_id>', methods=['POST'])
def add_new_favorite_character(id, character_id):
    user= User.query.get(id)

    character=Character.query.get(character_id)
    user.favorites_character.append(character)
    user.save()
    return "POSTEADO MI REY"

#DELETE a favorite character
@app.route('/users/<int:id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(id, character_id):
    user= User.query.get(id)
    character=Character.query.get(character_id)
    user.favorites_character.remove(character)
    user.save()
    return "ELIMINADO MI REY"

#POST a planet to favorites 
@app.route('/users/<int:id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(id, planet_id):
    user= User.query.get(id)

    planet=Planet.query.get(planet_id)
    user.favorites_planet.append(planet)
    user.save()
    return "POSTEADO MI REY"
    

#DELETE a favorite planet
@app.route('/users/<int:id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(id, planet_id):
    user= User.query.get(id)

    planet=Planet.query.get(planet_id)
    user.favorites_planet.remove(planet)
    user.save()
    return "ELIMINADO MI REY"


#POST a starship to favorites 
@app.route('/users/<int:id>/favorites/starships/<int:starship_id>', methods=['POST'])
def add_favorite_starship(id, starship_id):
    user= User.query.get(id)

    starship=Starship.query.get(starship_id)
    user.favorites_starship.append(starship)
    user.save()
    return "POSTEADO MI REY"
    

#DELETE a favorite starship
@app.route('/users/<int:id>/favorites/starships/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(id, starship_id):
    user= User.query.get(id)

    starship=Starship.query.get(starship_id)
    user.favorites_starship.remove(starship)
    user.save()
    return "ELIMINADO MI REY"


# DELETE a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user: return jsonify({"status": False, "msg":"User doesn't exist"}), 404
    user.delete()
    return jsonify({"status": True, "msg":"User deleted"}), 200

# DELETE a planet
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet: return jsonify({"status": False, "msg":"Planet doesn't exist"}), 404
    planet.delete()
    return jsonify({"status": True, "msg":"Planet deleted"})

# DELETE a character
@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character: return jsonify({"status": False, "msg":"Planet doesn't exist"}), 404
    character.delete()
    return jsonify({"status": True, "msg":"Character deleted"})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
