import json
from models import db, Brand, Model
from app import app

def populate_db():
    with app.app_context():
        db.create_all()
        with open('../models.json') as f:
            data = json.load(f)
            for item in data:
                brand = Brand.query.filter_by(name=item['brand_name']).first()
                if not brand:
                    brand = Brand(name=item['brand_name'])
                    db.session.add(brand)
                    db.session.commit()
                model = Model(id=item['id'], name=item['name'], average_price=item['average_price'], brand=brand)
                db.session.add(model)
            db.session.commit()

if __name__ == '__main__':
    populate_db()