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
	meal = meals.find_one({'_id' : ObjectId(meal_id)})
	return toJson(meal)

@app.route('/meals', methods=['POST'])
def add_meal():
	meals = mongo.db.meals
	meal = meals.insert_one({
		'name' : request.json['name'],
		'cuisine' : request.json['cuisine'],
		'difficulty' : request.json['difficulty'],
		'total_cooking_time' : request.json['total_cooking_time'],
		'ingredients' : request.json['ingredients'],
		'recipe' : request.json['recipe'],
		'ratings' : request.json['ratings']})
	# check to ensure that post worked correctly
	new_meal = meals.find_one({
		'name' : request.json['name'],
		'cuisine' : request.json['cuisine'],
		'difficulty' : request.json['difficulty'],
		'total_cooking_time' : request.json['total_cooking_time'],
		'ingredients' : request.json['ingredients'],
		'recipe' : request.json['recipe'],
		'ratings' : request.json['ratings']})
	return toJson(new_meal)
	
@app.route('/meals/<meal_id>', methods=['PATCH'])
def update_ratings(meal_id):
	meals = mongo.db.meals
	meals.update_one({'_id' : ObjectId(meal_id)}, {'$addToSet' : {'ratings' : request.json['ratings']}}) 
	updated_item = meals.find_one('id' : ObjectId(meal_id))
	return updated_item
	
@app.route('meals/<meal_id>', methods=['DELETE'])
def delete_meal(meal_id):	
	meals = mongo.db.meals
	result = meals.delete_one('_id' : ObjectId(meal_id))
	return (result.deleted_count == 1)
	
@app.route('/users', method=['GET'])
def get_all_users():
	users = mongo.db.users
	output = []
	for u in users.find():
		output.append(u)
	return toJson(output)
	
@app.route('/users/<user_id>', method=['GET'])
def get_user(user_id):
	users = mongo.db.users
	user = users.find_one('_id', ObjectId('user_id'))
	return toJson(user)
	
@app.route('/users', method=['POST'])
def add_user():
	users = mongo.db.users
	user = users.insert_one({
		'email' : request.json['email'],
		'password' : request.json['password'],
		'verified' : 'not_verified',
		'meal_plans' : []})
	new_user = users.find_one({
		'email' : request.json['email'],
		'password' : request.json['password'],
		'meal_plans' : []})
	return toJson(new_user)

@app.route('users/<user_id>', method=['PATCH'])
def verify_user(user_id):
	users = mongo.db.users
	users.update_one('_id' : ObjectId(user_id), {'verified' : 'verified'})
	updated_item = users.find_one('_id' : ObjectId(user_id))
	return toJson(updated_item)
	
@app.route('users/<user_id>', method=['DELETE']
def delete_user(user_id):
	users = mongo.db.users
	result = users.delete_one('_id' : ObjectId(user_id))
	return (result.deleted_count == 1)

if __name__ == '__main__':
	app.run(debug=True)