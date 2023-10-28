from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import DateTime
from flask_login import LoginManager,login_required, UserMixin,login_user,current_user
from flask import render_template, request, redirect, url_for, flash,session



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2345@localhost:5432/my_duka"
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    buying_price = db.Column(db.Numeric(precision=14, scale=2))
    selling_price = db.Column(db.Numeric(precision=14, scale=2))
    stock_quantity = db.Column(db.Numeric(precision=14, scale=2))


class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(precision=14, scale=2))
    created_at = db.Column(DateTime, default=db.func.current_timestamp())


class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

# Implement the required methods
def is_authenticated(self):
    return True

def is_active(self):
    return True

def is_anonymous(self):
    return False

def get_id(self):
    return str(self.id)


def authenticate_user(email, password):
    user = Users.query.filter_by(email=email).first()
    
    if user and user.password == password:
        # User exists and password matches (plaintext comparison)
        return user
    else:
        # User doesn't exist or password is incorrect
        return None


login_manager = LoginManager(app)
login_manager.login_view = "login" 

# Define the user_loader function
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


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
        new_product = Products(name=product_name, buying_price=buying_price,selling_price=selling_price,stock_quantity=stock_quantity)

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
@login_required
def sales():

    user = current_user
    # Use the query method to retrieve all records from the sales table
    sales = Sales.query.all()

    # You can now iterate over the 'sales' list to access the records
    data = [sale for sale in sales]    
    return render_template("sales.html", sales=data, user=user)




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        email = request.form['email']

        # Email Validation
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Email is already in use")
        elif not password or not email:
            flash("Please fill all the inputs")
        else:
            new_user = Users(full_name=full_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("You have registered successfully!")
            return redirect(url_for("products"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user and authenticate_user(email, password):
            # Successfully logged in, store user info in the session
            session['user_id'] = user.id
            flash("Logged in successfully!")
            return redirect(url_for("products"))
        else:
            flash("Invalid email or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Remove the user_id from the session to log out
    session.pop('user_id', None)
    flash("Logged out successfully")
    return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)