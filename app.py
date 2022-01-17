from ast import For
from flask import Flask
from flask import request
from flask import jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict
from playhouse.shortcuts import dict_to_model
from spellList import spell_list

db = PostgresqlDatabase('spells', user='postgres',
                        password='', host='localhost', port=5432)

# response = request.get('https://www.dnd5eapi.co/api/spells')
# response.json()


class BaseModel(Model):
    class Meta:
        database = db


class Spells(BaseModel):
    name = CharField()
    desc = TextField()
    spell_range = CharField()
    level = IntegerField()
    school = CharField()


db.connect()
db.drop_tables([Spells])
db.create_tables([Spells])

i = 0
while i < (len(spell_list)):
    for key in spell_list[i]:
        cast = Spells(name=spell_list[i]["name"], desc=spell_list[i]["desc"],
                      spell_range=spell_list[i]["spell_range"], level=spell_list[i]["level"], school=spell_list[i]["school"])
        cast.save()
        i += 1


app = Flask(__name__)


@app.route('/spells', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/spells/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def spell(id=None):
    # GET by ID
    if request.method == 'GET':
        if id:
            spell = Spells.get(Spells.id == id)
            cast = model_to_dict(spell)
            return jsonify(cast)
        # GET all
        else:
            spell = []
            # Iterate over a query that gets every Spell
            for casts in Spells.select():
                # Convert each spell from Python object to Dictionary
                spell.append(model_to_dict(casts))
            # Convert list of dictionaries into JSON and return to server
            return jsonify(spell)

        # POST request
    if request.method == 'POST':
        spell = request.get_json()
        spell = dict_to_model(Spells, spell)
        spell.save()
        spell = model_to_dict(spell)
        return jsonify(spell)

        # DELETE request
    if request.method == 'DELETE':
        spell = Spells.get(Spells.id == id)
        spell.delete_instance()
        return jsonify({'Deleted': True})

        # PUT Request
    if request.method == 'PUT':
        updated_spell = request.get_json()
        spell = Spells.get(Spells.id == id)
        spell.name = updated_spell['name']
        spell.desc = updated_spell['desc']
        spell.spell_range = updated_spell['spell_range']
        spell.level = updated_spell['level']
        spell.school = updated_spell['school']
        spell.save()
        spell = model_to_dict(spell)
        return jsonify(spell)


@app.route('/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def index():
    if request.method == 'GET':
        return jsonify({"message": "D&D 5E spells"})
    else:
        return jsonify({"message": "Hello, world!"})


app.run(port=9000, debug=True)
