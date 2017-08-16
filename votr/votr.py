from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users


votr = Flask(__name__)

votr.config.from_object('config')

db.init_app(votr)
db.create_all(app=votr)


@votr.route('/')
def home():
    return render_template('index.html')


@votr.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # Get signup form values
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password = generate_password_hash(password)
        # Add user to the database
        user = Users(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        # Display success message and redirect to homepage
        flash('Thank you for signing up!')
        return redirect(url_for('home'))

    return render_template('signup.html')


@votr.route('/login', methods=['POST'])
def login():
    # Get login form values
    username = request.form['username']
    password = request.form['password']
    # Query database for username
    user = Users.query.filter_by(username=username).first()
    # Check password if username exists
    if user:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session['user'] = username
            flash('Login successful!')
    else:
        flash('Username or password is incorrect.', 'error')

    return redirect(url_for('home'))


@votr.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        flash('We hope to see you again!')

    return redirect(url_for('home')) 


@votr.route('/polls')
def polls():
    return render_template('polls.html')


if __name__=='__main__':
    votr.run()