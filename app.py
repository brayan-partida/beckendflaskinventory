from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
# mysql://ubfjdy1y2tivbwmb:SUfWNAfPpbxce0cP6HPO@bmznnvnnuh65bmolx7hn-mysql.services.clever-cloud.com:3306/bmznnvnnuh65bmolx7hn
app = Flask(__name__)


# mysql+pymysql://ubfjdy1y2tivbwmb:SUfWNAfPpbxce0cP6HPO@bmznnvnnuh65bmolx7hn-mysql.services.clever-cloud.com/bmznnvnnuh65bmolx7hn
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ubfjdy1y2tivbwmb:SUfWNAfPpbxce0cP6HPO@bmznnvnnuh65bmolx7hn-mysql.services.clever-cloud.com/bmznnvnnuh65bmolx7hn'
# 'mysql+pymysql://root:@localhost/servicio_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    postcode = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    # relacion de ordenes y clientes
    orders = db.relationship("Order", backref='customer')
    # relacion de uno a muchos

    # relacion de ordenes y clientes


order_product = db.Table('order_product',
                         db.Column('order_id', db.Integer, db.ForeignKey(
                             'order.id'), primary_key=True),
                         db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True))
# relacion de muchos a muchos


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "customer.id"), nullable=False)
    # ANCHOR relacion orden => costumer one to many

    products = db.relationship("Product", secondary=order_product)
    # ANCHOR  realtion many to many
# NOTE finish models===============================================>


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    price = db.Column(db.Integer, nullable=False)


db.create_all()  # crea toda la base de datos


class CustomerSchema(ma.Schema):
    class Meta:
        model = Customer


@app.route("/user", methods=['POST'])
def postuser():
    first_names = request.json['first_name']
    last_names = request.json['last_name']
    citys = request.json['city']
    postcodes = request.json['postcode']
    emails = request.json['email']
    person = Customer(first_name=first_names,
                      last_name=last_names,
                      city=citys,
                      postcode=postcodes,
                      email=emails)

    db.session.add(person)
    db.session.commit()
    return "se inserto"


@app.route("/user", methods=['GET'])
def getuser():
    oneCustomer = Customer.query.first()
    customer_schema = CustomerSchema()
    output = customer_schema.dump(oneCustomer).data()
    return jsonify({"customer": output})


if __name__ == "__main__":
    app.run(debug=True)
