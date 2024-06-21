here are the steps you can follow:
1. Setup Your Project
Assuming you have already set up a virtual environment and installed necessary dependencies (Flask, Flask-WTF, Flask-Migrate, psycopg2-binary, email-validator, python-dotenv), proceed with the following steps.
2. Setting up .env
Ensure your .env file contains your database URL in the following format:DATABASE_URL=postgresql://your_username:your_password@localhost:5432/car-collection
3. Create User Model (app/models.py)
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.email}>'
4. Create Signup Form (app/forms.py)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
5. Create Signup Route (app/routes/authentication.py)
from flask import Blueprint, render_template, redirect, url_for
from app.forms import SignupForm
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Create a new user instance
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=form.password.data)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Optionally, you may redirect to a success page or login page
        return redirect(url_for('auth.signup_success'))

    return render_template('signup.html', form=form)

@auth_bp.route('/signup-success')
def signup_success():
    return "Signup successful! You can now login."
6. Create Database Initialization (manage.py)
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
7. Initialize Your Flask App (app/__init__.py)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    csrf.init_app(app)

    from app.routes.authentication import auth_bp
    app.register_blueprint(auth_bp)

    return app
8. Create Signup HTML Template (app/templates/signup.html)
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sign Up</title>
</head>
<body>
    <h2>Sign Up</h2>
    <form method="POST" action="{{ url_for('auth.signup') }}">
        {{ form.hidden_tag() }}
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=32) }}<br>
            {% for error in form.email.errors %}
                <span style="color: red;">{{ error }}</span><br>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
                <span style="color: red;">{{ error }}</span><br>
            {% endfor %}
        </p>
        <p>
            {{ form.first_name.label }}<br>
            {{ form.first_name(size=32) }}<br>
            {% for error in form.first_name.errors %}
                <span style="color: red;">{{ error }}</span><br>
            {% endfor %}
        </p>
        <p>
            {{ form.last_name.label }}<br>
            {{ form.last_name(size=32) }}<br>
            {% for error in form.last_name.errors %}
                <span style="color: red;">{{ error }}</span><br>
            {% endfor %} </p>
        <p>{{ form.submit() }}</p> </form </body></html>
9. Running Your Application
Make sure your PostgreSQL server is running and your database (car-collection) is set up. Then, run the following commands in your terminal:
bash
Copy code
python manage.py db init  # Initialize migrations (only once)
python manage.py db migrate  # Create initial migration
python manage.py db upgrade  # Apply initial migration

python manage.py runserver  # Run the Flask development server
