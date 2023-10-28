from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import DateTime
from flask_login import LoginManager,login_required, UserMixin,login_user


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2345@localhost:5432/my_duka"
db = SQLAlchemy(app)


class Products(db.Model,UserMixin):
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


class Users(db.Model):
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
