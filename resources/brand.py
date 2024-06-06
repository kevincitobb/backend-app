from flask import Blueprint, request, jsonify
from models import db, Brand
from schemas import BrandSchema, ModelSchema

brand_bp = Blueprint('brands', __name__)
brand_schema = BrandSchema()
brands_schema = BrandSchema(many=True)
models_schema = ModelSchema(many=True)

@brand_bp.route('/', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    return jsonify(brands_schema.dump(brands))

@brand_bp.route('/<int:id>/models', methods=['GET'])
def get_models_by_brand(id):
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"error": "Brand not found"}), 404
    return jsonify(models_schema.dump(brand.models))

@brand_bp.route('/', methods=['POST'])
def add_brand():
    name = request.json['name']
    if Brand.query.filter_by(name=name).first():
        return jsonify({"error": "Brand name already exists"}), 400
    new_brand = Brand(name=name)
    db.session.add(new_brand)
    db.session.commit()
    return brand_schema.jsonify(new_brand), 201