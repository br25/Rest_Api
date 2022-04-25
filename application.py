from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)




class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))


    def __repr__(self):
        return f"{self.name} + {self.description}"


@app.route("/")
def index():
    return 'Hello, Mars'


@app.route("/fruit")
def get_item():
    fruits = Fruit.query.all()

    output=[]
    for fruit in fruits:
        fruit_data = {'name': fruit.name, 'description': fruit.description}

        output.append(fruit_data)

    return {"Fruit" : output}


@app.route('/fruit/<id>')
def get_item_id(id):
    fruit = Fruit.query.get_or_404(id)
    return {"name": fruit.name, "description": fruit.description}


@app.route('/fruit', methods=['POST'])
def add_item():
    fruit = Fruit(name=request.json['name'],
        description=request.json['description'])
    db.session.add(fruit)
    db.session.commit()
    return {'id': fruit.id}

@app.route('/fruit/<id>', methods=['DELETE'])
def delete_item(id):
    fruit = Fruit.query.get(id)
    if fruit is None:
        return {"error": "not Found Fruit"}

    db.session.delete(fruit)
    db.session.commit()
    return{"message": "success Delete"}



