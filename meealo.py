# code for mongodb

from flask import Flask, jsonify, request, json, abort, render_template
from flask_pymongo import PyMongo
from flask_restplus import Resource
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
#	mongo.db.users.create_index("email", unique=True)
	meals = get_all_meals()
	return render_template('index.html', meals=meals)

def get_all_meals():
	meals = mongo.db.meals
	output = []
	for m in meals.find():
		output.append(m)
	return output

# meal data section
@app.route('/meals', methods=['GET'])
def get_all_meals_JSON():
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

# add a new meal to the database
# requires ingredients list to be separated by a -- and recipe steps by --
# can be changed later if a better delimiter is thought of
@app.route('/meals', methods=['POST'])
def add_meal():
	meals = mongo.db.meals
	ingredients = [y for y in (x.strip() for x in request.form['ingredients'].split('--')) if y]
	recipe = [y for y in (x.strip() for x in request.form['recipe'].split('--')) if y]
	meal = meals.insert_one({
		'name' : request.form['name'],
		'cuisine' : request.form['cuisine'],
		'difficulty' : request.form['difficulty'],
		'total_cooking_time' : request.form['total_cooking_time'],
		'ingredients' : ingredients,
		'recipe' : recipe,
		'ratings' : {
			"0": "0",
			"1": "0",
			"2": "0",
			"3": "0",
			"4": "0",
			"5": "0",
			"avg": "0"
		}})
	# check to ensure that post worked correctly
	new_meal = meals.find_one({
		'name' : request.form['name'],
		'cuisine' : request.form['cuisine'],
		'difficulty' : request.form['difficulty'],
		'total_cooking_time' : request.form['total_cooking_time'],
		'ingredients' : ingredients,
		'recipe' : recipe})
	return toJson(new_meal)

# sets document field to new value, only does one at a time	
# e.g. {"patch_field":"ratings.0", "patch_value":"4"}
@app.route('/meals/<meal_id>', methods=['PATCH'])
def update_ratings(meal_id):
	meals = mongo.db.meals
	meals.update_one({'_id' : ObjectId(meal_id)}, {"$set" : {request.json['patch_field'] : request.json['patch_value']}}, upsert=False) 
	updated_item = meals.find_one({'_id' : ObjectId(meal_id)})
	return toJson(updated_item)

	
@app.route('/meals/<meal_id>', methods=['DELETE'])
def delete_meal(meal_id):	
	meals = mongo.db.meals
	result = meals.delete_one({'_id' : ObjectId(meal_id)})
	if result.deleted_count == 1:
		return Response(status=201)
	else:
		return abort(404)

# user data section	
@app.route('/users', methods=['GET'])
def get_all_users():
	users = mongo.db.users
	output = []
	for u in users.find():
		output.append(u)
	return toJson(output)
	
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
	users = mongo.db.users
	user = users.find_one('_id', ObjectId('user_id'))
	return toJson(user)
	
@app.route('/users', methods=['POST'])
def add_user():
	users = mongo.db.users
	user = users.insert_one({
		'email' : request.form['email'],
		'name' : request.form['name'],
		'password' : request.form['password'],
		'verified' : 'not_verified',
		'meal_plans-ids' : []})
	new_user = users.find_one({
		'email' : request.form['email']})
	return toJson(new_user)

# only does update for verification and meal plan adding	
@app.route('/users/<user_id>', methods=['PATCH'])
def verify_user(user_id):
	users = mongo.db.users
	if request.json['patch'] == 'verified':
		users.update_one({'_id' : ObjectId(user_id)}, {'verified' : 'verified'}, upsert=False)
	else:	
		meal_plan_ids = [y for y in (x.strip() for x in request.form['meal_plan_ids'].split('--')) if y]
		users.update_one({'_id' : ObjectId(user_id)}, {'meal_plan_ids' : meal_plan_ids}, upsert=False)
	updated_item = users.find_one({'_id' : ObjectId(user_id)})
	return toJson(updated_item)

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
	users = mongo.db.users
	result = users.delete_one({'_id' : ObjectId(user_id)})
	if result.deleted_count == 1:
		return Response(status=201)
	else:
		return abort(404)

# meal plan data section	
@app.route('/meal_plans', methods=['GET'])
def get_meal_plans():
	meal_plans = mongo.db.meal_plans
	output = []
	for m in meal_plans():
		output.append(m)
	return toJson(output)
	
@app.route('/meal_plans/<meal_plan_id>', methods=['GET'])
def get_meal_plan(meal_plan_id):
	meal_plans = mongo.db.meal_plans
	meal_plan = meal_plans.find_one({'_id' : ObjectId(meal_plan_id)})
	return toJson(meal_plan)

@app.route('/meal_plans', methods=['POST'])
def add_meal_plan():
	meal_plans = mongo.db.meal_plans
	meal_ids = [y for y in (x.strip() for x in request.form['meal_ids'].split('--')) if y]	
	meal_plan = meal_plans.insert_one({
		'duration' : request.json['duration'],
		'start_date' : request.json['start_date'],
		'meal_ids' : meal_ids})
	new_meal_plan = meals.find_one({
		'duration' : request.json['duration'],
		'start_date' : request.json['start_date'],
		'meal_ids' : meal_ids})
	return toJson(new_meal_plan)

@app.route('/meal_plans/<meal_plan_id>', methods=['PATCH'])
def modify_meal_plan(meal_plan_id):
	meal_plans = mongo.db.meal_plans
	meal_ids = [y for y in (x.strip() for x in request.form['meal_ids'].split('--')) if y]	
	meal_plans.update_one({'_id' : ObjectId(meal_plan_id)}, {'meal_plan_id' : meal_ids})
	updated_meal_plan = meal_plans.find_one({'_id' : ObjectId(meal_plan_id)})
	return toJson(updated_meal_plan)
	
if __name__ == '__main__':
	app.run(debug=True)
