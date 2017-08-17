from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from models import db, Users, Topics, Options, Polls


votr = Flask(__name__)

votr.config.from_object('config')

db.init_app(votr)
db.create_all(app=votr)

migrate = Migrate(votr, db, render_as_batch=True)

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


@votr.route('/api/polls', methods=['GET', 'POST'])
def api_polls():
    if request.method == 'POST':
        poll = request.get_json()
        for key, value in poll.items():
            if not value:
                return jsonify({"message": "ERROR: value for {} is empty".format(key)})
        title = poll['title']
        options_query = lambda option : Options.query.filter(Options.name.like(option))
        options = [Polls(option=Options(name=option)) if options_query(option)==0 else Polls(option=options_query(option).first()) for option in poll['options']]
        new_topic = Topics(title=title, options=options)

        db.session.add(new_topic)
        db.session.commit()
        return jsonify({'message':'Poll was created successfuly'})
    else:
        polls = Topics.query.join(Polls).all()
        all_polls = {'Polls': [poll.to_json() for poll in polls]}
        return jsonify(all_polls)

@votr.route('/api/polls/options')
def api_options():
    all_options = [option.to_json() for option in Options.query.all()]
    return jsonify(all_options)

@votr.route('/api/polls/vote', methods=['PATCH'])
def api_votes():
    poll = request.get_json()
    poll_title, vote_option = (poll['poll_title'], poll['option'])
    join_tables = Polls.query.join(Topics).join(Options)
    option = join_tables.filter(Topics.title.like(poll_title)).filter(Options.name.like(vote_option)).first()
    if option:
        option.vote_count += 1
        db.session.commit()
        return jsonify({"message": "Thank you for voting!"})
    
    return jsonify({'message': "Option or poll was not found. Please try again."}) 

if __name__=='__main__':
    votr.run()
