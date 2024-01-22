from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import logging
import random
from config import Config
from database import db
from users import Users
from bookings import Bookings
from datetime import datetime, timedelta

# Configure basic logging to print messages to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#set up the flask app and the database
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'
db.init_app(app)

# Configure your PostgreSQL database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql@localhost/ClassroomBookingSystem'


def capitalize_first_and_last(string):
    # Split the string into words
    if string is None:
        return ""

    words = string.split()

    # Check if there are any words in the string
    if len(words) > 0:
        # Capitalize the first letter of the first word
        first_word = words[0].capitalize()

        # Capitalize the first letter of the last word
        last_word = words[-1].capitalize()
        first_letter = first_word[0]
        last_letter = last_word[0]
        # Return the modified string
        print(first_letter)
        print(last_letter)
        return f"{first_word}{last_word}"

    # If the string is empty, return an empty string
    return ""


@app.route('/', methods=['GET'])
def index():
    logging.info("Entry Point")

    return render_template('/login.html')


@app.route('/create', methods=['GET'])
def create():
    logging.info("Create Point")

    return render_template('/register/form.html')

@app.route('/confirmation')
def confirmation():
    logging.info("Confirmation Point")
    user_id = session['user_id']
    redirect_url = request.args.get('redirect_url')
    user = Users.query.filter_by(userid=user_id).first()


    #delete the user_id from the session to ensure that the user logs in afterwards
    session.pop('user_id', None)

    return render_template('/register/confirmation.html',
                           username=user.username,
                           email=user.email,
                           password=user.password,
                           redirect_url=redirect_url)

@app.route('/register', methods=['POST'])
def register():
    logging.info("Register Point")
    if request.method == 'POST':
        try:
            logging.info("Register Point2")
            # Retrieve form data using request.json for JSON data or request.form for form data

            username = request.form['username']
            print("username:",username)
            email = request.form['email']
            print("email:",email)
            password = request.form['password']
            print("password:",password)
            if not username or not email or not password:
                print("Form returned nothing")
                num = str(random.randint(0,222))
                username = "DefaultUser" + num
                email = "DefaultUser" + num + "@gmail.com"
                password = "DefaultUserpswrd" + num

            # Process the form data as needed
            # Create a new User instance and add it to the database
            new_user = Users(
                username=username,
                email=email,  # Assuming Email is used as an example for account_user_name
                password=password,
                admin=False,
            )

            print(new_user)
            db.session.add(new_user)
            db.session.commit()

            # Log the new user information
            app.logger.info(f"New User: {str(new_user)}")

            # set the session id so the confirmation screen can use it
            session['user_id'] = new_user.userid

            # Redirect to the /confirmation route
            return redirect(url_for('confirmation'))

        except Exception as e:
            error_message = {"error": str(e)}
            return jsonify(error_message), 400  # Respond with an error message if there's an issue

    # Add an additional response if the request method is not 'POST'
    return jsonify({"error": "Invalid request method"}), 405

@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        try:
            # Retrieve form data using request.form
            account_email = request.form['accountEmail']
            account_password = request.form['accountUserPassword']
            logging.info(account_email)
            logging.info(account_password)
            # Query the database for the user with the provided email
            user = Users.query.filter_by(email=account_email).first()

            # Check if the user exists and the password is correct
            if user and user.password == account_password:
      #
      # Redirect to the home page if credentials are correct
                logging.info("Logged in")
                session['user_id'] = user.userid
                return redirect(url_for('home'))

            # Return an error message if credentials are incorrect
            error_message = {"error": "Invalid email or password"}
            return jsonify(error_message), 401

        except Exception as e:
            error_message = {"error": str(e)}
            return jsonify(error_message), 400  # Respond with an error message if there's an issue

    # Add an additional response if the request method is not 'POST'
    return jsonify({"error": "Invalid request method"}), 405

@app.route('/home', methods=['GET'])
def home():
    logging.info("Home Point")

    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    user = Users.query.filter_by(userid=user_id).first()
    if user is None:
        return redirect(url_for('index'))

    logging.info(user_id)
    return render_template('/home.html')

@app.route('/createbooking', methods=['GET'])
def createbooking():
    logging.info("Create Booking Point")

    return render_template('/booking.html')
@app.route('/book', methods=['POST'])
def book():
    logging.info("Booking Point")

    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    user = Users.query.filter_by(userid=user_id).first()
    if user is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Extract data from form

        classroom = request.form['room']
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%m/%d/%Y')
        start_time_str = request.form['start_time']
        duration = float(request.form['duration'])

        # Combine date and start time
        start_time = datetime.combine(date, datetime.strptime(start_time_str, '%H:%M').time())
        end_time = start_time + timedelta(hours=duration)

        logging.info("Creating Booking Object")

        try:
            # Create booking object
            booking = Bookings(
                user_id=user_id,
                classroom=classroom,
                title=title,
                date=date,
                start_time=start_time,
                end_time=end_time,
                status='Pending'  # Default status, adjust as needed
            )

            # Add booking to the database
            db.session.add(booking)
            db.session.commit()

        except Exception as e:
            error_message = {"error": str(e)}
            return jsonify(error_message), 400  # Respond with an error message if there's an issue

        # Redirect or return a response
        return redirect(url_for('mybookings'))  # Redirect to a success page, or handle as needed

    return 'Invalid Method', 405


@app.route('/mybookings', methods=['GET'])
def mybookings():

    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    user = Users.query.filter_by(userid=user_id).first()
    if user is None:
        return redirect(url_for('index'))

    # Query the database for bookings by the user
    bookings = Bookings.query.filter_by(user_id=user_id).all()
    return render_template('mybookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run()
