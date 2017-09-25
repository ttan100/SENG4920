# code for mongodb

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restplus import Resource
import json
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)

# connect to plannerdb in external database
app.config['MONGO_DBNAME'] = 'plannerdb'
app.config['MONGO_URI'] = 'mongodb://meealo:meealo123@ds139904.mlab.com:39904/plannerdb'

mongo = PyMongo(app)

# dumps mongo data object as json
def toJson(data):
	return json.dumps(data, default=json_util.default)

# test that the index uri works
@app.route('/')
def hello():
	return 'Hello world!'

@app.route('/meals', methods=['GET'])
def get_all_meals():
	meals = mongo.db.meals
	output = []
	for m in meals.find():
		output.append(m)
	return toJson(output)
	
@app.route('/meals/<meal_id>', methods=['GET'])
def get_meal(meal_id):
	meals = mongo.db.meals
	q = meals.find_one({'_id' : ObjectId(meal_id)})
	return toJson(q)

@app.route('/meals', methods=['POST'])
def add_meal():
	meals = mongo.db.meals
	name = request.json['name']
	cuisine = request.json['cuisine']
	difficulty = request.json['difficulty']
	cooktime = request.json['
	meal_id = meals.insert({
		'name' : request.json['name'],
		'cuisine' : request.json['cuisine'],
		'difficulty' : request.json['difficulty'],
		'total_cooking_time' : request.json['total_cooking_time'],
		'ingredients' : request.json['ingredients'],
		'recipe' : request.json['recipe'],
		'ratings' : request.json['ratings']})
	# check to ensure that post worked correctly
	new_meal = meals.find_one({'_id' : meal_id})
	output = {'name' : new_meal['name'], 'type' : new_meal['type']}
	return jsonify({'result' : output})
	
@app.route('/meals', methods=['PATCH'])
def modify_meal():
	meals = mongo.db.meals
	type = request.json()['type']
	
@app.route('meals/<meal_id>', methods=['DELETE'])
	
if __name__ == '__main__':
	app.run(debug=True)