from flask import Flask, request, jsonify
from models import db, Brand, Model
from schemas import ma, BrandSchema, ModelSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

# Import and register blueprints
from resources.brand import brand_bp
from resources.model import model_bp
app.register_blueprint(brand_bp, url_prefix='/brands')
app.register_blueprint(model_bp, url_prefix='/models')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)