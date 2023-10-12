from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2345@localhost:5432/duka"


db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.Integer)

# users = db.session.execute(db.select(Users).order_by(Users.full_name)).scalars()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data from the request
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Create a new User instance with the form data
        new_user = Users(full_name=full_name, email=email, password=password)

        # Add the new user to the database session
        db.session.add(new_user)

        # Commit the changes to the database
        db.session.commit()

        return redirect("/")

    # Use the query method to retrieve all records from the Users table
    users = Users.query.all()

    # You can now iterate over the 'users' list to access the records
    data = [user for user in users]

    return render_template("test.html", users=data)



app.run(debug=True)
