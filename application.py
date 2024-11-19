
# make sure to install Flask and SQLAlchemy
# pip install Flask
# pip install flask_sqlalchemy
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# # Initialize the Flask server
# # the __name__ variable is a special variable in Python that 
# # is used to determine if the code is being run from the
# # command line or if it has been imported into another file
app = Flask(__name__)

# # Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

# # First, create a model
# # A model is a representation of a table in a database
# # SQLAlchemy is a library that allows you to interact with databases using Python
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(120))

    # ORM - Object Relational Mapping - allows you to interact with the database
    def __repr__(self):
        return f'{self.name} - {self.description}'
    
# # Decorators are a way to add functionality to existing functions
# # without modifying their code
# # this decorator creates a route (URL) and says run the following function
# # when someone (or a user) goes to this route
    
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)
        
    return {'drinks': output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id) # if the drink does not exist, return a 404 error ("not found")
    return {'name': drink.name, 'description': drink.description}

# adding a new drink
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=requests.json['name'], description=requests.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

# removing a drink
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {'error': 'not found'}
    
    db.session.delete(drink)
    db.session.commit()
    
    return {'message': 'deleted'}
