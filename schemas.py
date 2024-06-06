from flask_marshmallow import Marshmallow
from models import Brand, Model

ma = Marshmallow()

class BrandSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Brand
        include_relationships = True
        load_instance = True

class ModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        include_fk = True
        load_instance = True