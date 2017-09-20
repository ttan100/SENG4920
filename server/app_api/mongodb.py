# code for mongodb

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

# connect to plannerdb in localhost
app.config['MONGO_DBNAME'] = 'plannerdb'
app.config['MONGO_URI'] = 'mongodb://meealo:meealo123@ds139904.mlab.com:39904/plannerdb'

mongo = PyMongo(app)

@app.route('/meals/add