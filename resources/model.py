from flask import Blueprint, request, jsonify
from models import db, Model, Brand
from schemas import ModelSchema

model_bp = Blueprint('models', __name__)
model_schema = ModelSchema()
models_schema = ModelSchema(many=True)

@model_bp.route('/', methods=['GET'])
def get_models():
    greater = request.args.get('greater', type=int)
    lower = request.args.get('lower', type=int)
    query = Model.query
    if greater:
        query = query.filter(Model.average_price > greater)
    if lower:
        query = query.filter(Model.average_price < lower)
    models = query.all()
    return jsonify(models_schema.dump(models))

@model_bp.route('/<int:id>', methods=['PUT'])
def update_model(id):
    model = Model.query.get(id)
    if not model:
        return jsonify({"error": "Model not found"}), 404
    average_price = request.json.get('average_price')
    if average_price and average_price < 100000:
        return jsonify({"error": "Average price must be greater than 100,000"}), 400
    model.average_price = average_price
    db.session.commit()
    return model_schema.jsonify(model)

@model_bp.route('/<int:brand_id>', methods=['POST'])
def add_model(brand_id):
    name = request.json['name']
    average_price = request.json.get('average_price')
    brand = Brand.query.get(brand_id)
    if not brand:
        return jsonify({"error": "Brand not found"}), 404
    if Model.query.filter_by(name=name, brand_id=brand_id).first():
        return jsonify({"error": "Model name already exists for this brand"}), 400
    if average_price and average_price < 100000:
        return jsonify({"error": "Average price must be greater than 100,000"}), 400
    new_model = Model(name=name, average_price=average_price, brand=brand)
    db.session.add(new_model)
    db.session.commit()
    return model_schema.jsonify(new_model), 201