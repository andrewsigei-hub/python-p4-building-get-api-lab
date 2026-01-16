#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# Route 1: GET /bakeries - returns all bakeries with nested baked goods
@app.route('/bakeries')
def bakeries():
    # Get all bakeries from database
    all_bakeries = Bakery.query.all()
    
    # Convert each bakery to dictionary (includes nested baked_goods)
    bakeries_list = [bakery.to_dict() for bakery in all_bakeries]
    
    # Return JSON response
    return make_response(jsonify(bakeries_list), 200)

# Route 2: GET /bakeries/<int:id> - returns single bakery with nested baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Find the bakery with this ID
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    # Check if bakery exists FIRST before trying to use it
    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    
    # Return the bakery with nested baked_goods
    return make_response(jsonify(bakery.to_dict()), 200)

# Route 3: GET /baked_goods/by_price - returns all baked goods sorted by price (descending)
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query all baked goods and sort by price in descending order (highest to lowest)
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    # Convert each baked good to dictionary (includes nested bakery info)
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    
    # Return JSON response
    return make_response(jsonify(baked_goods_list), 200)

# Route 4: GET /baked_goods/most_expensive - returns the single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query baked goods sorted by price (descending) and get only the first one
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    # If no baked goods exist, return 404 error
    if most_expensive is None:
        return make_response(jsonify({"error": "No baked goods found"}), 404)
    
    # Convert to dictionary (includes nested bakery info)
    return make_response(jsonify(most_expensive.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)