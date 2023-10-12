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
@app.route("/products",methods=["GET","POST"])
def products():
    if request.method == "POST":
        product_name = request.form["product_name"]
        buying_price = float(request.form["buying_price"])
        selling_price = float(request.form["selling_price"])
        stock_quantity = int(request.form["stock_quantity"])

        # Create a new product instance with the form data
        new_product = Products(product_name=product_name, buying_price=buying_price,selling_price=selling_price,stock_quantity=stock_quantity)

        # Add the new product to the database session
        db.session.add(new_product)

        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for("products"))

    # Use the query method to retrieve all records from the products table
    products = Products.query.all()

    # You can now iterate over the 'products' list to access the records
    data = [product for product in products]    
    return render_template("products.html", products=data )

# get sales
@app.route("/sales",methods=["GET"])
def sales():
    # Use the query method to retrieve all records from the sales table
    sales = Sales.query.all()

    # You can now iterate over the 'sales' list to access the records
    data = [sale for sale in sales]    
    return render_template("sales.html", sales=data )
   

app.run(debug=True)