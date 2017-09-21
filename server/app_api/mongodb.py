# code for mongodb

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restplus import Resource

app = Flask(__name__)

# connect to plannerdb in external database
app.config['MONGO_DBNAME'] = 'plannerdb'
app.config['MONGO_URI'] = 'mongodb://meealo:meealo123@ds139904.mlab.com:39904/plannerdb'

mongo = PyMongo(app)

@app.route('/')
def hello():
	return 'Hello world!'

@app.route('/meals', methods=['GET'])
def get_all_meals():
	meals = mongo.db.meals
	output = []
	for m in meals.find():
		output.append({'name' : m['name'], 'type' : m['type']})
	return jsonify({'result' : output})
	
@app.route('/meals/<name>', methods=['GET'])
def get_meal():
	meals = mongo.db.meals
	q = meals.find_one({'name' : name})
	if q:
		output = {'name' : m['name'], 'type' : m['type']}
	else:
		output = 'No meal with that name'
	return jsonify({'result' : output})

@app.route('/meals', methods=['POST'])
def add_meal():
	meals = mongo.db.meals
	name = request.json['name']
	type = request.json['type']
	meal_id = meals.insert({'name' : name, 'type' : type})
	# check to ensure that post worked correctly
	new_meal = meals.find_one({'_id' : meal_id})
	output = {'name' : new_meal['name'], 'type' : new_meal['type']}
	return jsonify({'result' : output})
	
@app.route('/meals', methods=['PATCH'])
def modify_meal():
	meals = mongo.db.meals
	type = request.json()['type']
	
	
if __name__ == '__main__':
	app.run(debug=True)