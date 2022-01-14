from flask import Flask
from flask import request
from flask import jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict
from spellList import spell_list

db = PostgresqlDatabase('spells', user='postgres',
                        password='', host='localhost', port=5432)

response = request.get('https://www.dnd5eapi.co/api/spells')
response.json()


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

spells = Spells(name=spell_list.name, desc=spell_list.desc,
                spell_range=spell_list.range, level=spell_list.level, school=spell_list.school)
spells.save()


app = Flask(__name__)


@app.route('/spells', methods=['GET'])
@app.route('/spells/<index>', methods=['GET'])
def spell(index=None):
    if index:
        spell = Spells.get(Spells.index == index)
        spell = model_to_dict(spell)
        return jsonify(spell)
    else:
        spell = []
        # Iterate over a query that gets every Spell
        for spell in Spells.select():
            # Convert each spell from Python object to Dictionary
            spell.append(model_to_dict(spell))
        # Convert list of dictionaries into JSON and return to server
        return jsonify(spell)


@app.route('/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def index():
    if request.method == 'GET':
        return jsonify({"message": "Hello GET"})
    else:
        return jsonify({"message": "Hello, world!"})


app.run(port=9000, debug=True)
