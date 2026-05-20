import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# IMAGE UPLOAD FOLDER
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# PRODUCT TABLE
class Product(db.Model):

id = db.Column(db.Integer, primary_key=True)

name = db.Column(db.String(100), nullable=False)

category = db.Column(db.String(50), nullable=False)

quantity = db.Column(db.Integer, nullable=False)

price = db.Column(db.Float, nullable=False)

image = db.Column(db.String(200), nullable=True)

# SALES TABLE
class Sale(db.Model):

id = db.Column(db.Integer, primary_key=True)

product_name = db.Column(db.String(100))

quantity_sold = db.Column(db.Integer)

total_price = db.Column(db.Float)

# CREATE DATABASE
with app.app_context():
db.create_all()

# HOME PAGE
@app.route("/")
def index():

products = Product.query.all()

return render_template("index.html", products=products)

# ADD PRODUCT
@app.route("/add", methods=["GET", "POST"])
def add_product():

if request.method == "POST":

name = request.form["name"]
category = request.form["category"]
quantity = int(request.form["quantity"])
price = float(request.form["price"])

# IMAGE
file = request.files["image"]

filename = file.filename

file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

product = Product(
name=name,
category=category,
quantity=quantity,
price=price,
image=filename
)

db.session.add(product)
db.session.commit()

return redirect(url_for("index"))

return render_template("add_product.html")

# SALES PAGE
@app.route("/sales", methods=["GET", "POST"])
def sales():

products = Product.query.all()

if request.method == "POST":

product_id = request.form["product_id"]

quantity_sold = int(request.form["quantity_sold"])

product = Product.query.get(product_id)

if product.quantity >= quantity_sold:

product.quantity -= quantity_sold

total = quantity_sold * product.price

sale = Sale(
product_name=product.name,
quantity_sold=quantity_sold,
total_price=total
)

db.session.add(sale)
db.session.commit()

return redirect(url_for("sales"))

sales_report = Sale.query.all()

return render_template(
"sales.html",
products=products,
sales=sales_report
)

if __name__ == "__main__":
app.run(debug=True)