from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import DateTime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2345@localhost:5432/duka"

db = SQLAlchemy(app)

class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    buying_price = db.Column(db.Numeric(precision=14, scale=2))
    selling_price = db.Column(db.Numeric(precision=14, scale=2))
    stock_quantity = db.Column(db.Numeric(precision=14, scale=2))

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(precision=14, scale=2))
    created_at = db.Column(DateTime, default=db.func.current_timestamp())

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

# index route
@app.route("/")
def index():
    return render_template("landing.html")


# get products
@app.route("/products",methods=["GET"])
def products():
    # Use the query method to retrieve all records from the Users table
    products = Products.query.all()

    # You can now iterate over the 'users' list to access the records
    data = [product for product in products]    
    return render_template("products.html", products=data )
   

app.run(debug=True)