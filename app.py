from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import logging
import random
from flask_sqlalchemy import SQLAlchemy

# Configure basic logging to print messages to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/ClassroomBookingSystem'
db = SQLAlchemy(app)
print("Hello world")


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

        # Return the modified string
        return f"{first_word} {last_word}"

    # If the string is empty, return an empty string
    return ""

class Users(db.Model):
    userid = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f"User: {self.userid}, {self.username}, {self.email}, {self.password}, {self.admin}"


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

            username = request.args.get('username')
            email = request.args.get('email')
            password = request.args.get('password')
            userid = capitalize_first_and_last(username) + str(random.randint(1000,9999))
            if not username:
                num = str(random.randint(0,222))
                username = "DefaultUser" + num
                email = "DefaultUser" + num + "@gmail.com"
                password = "DefaultUserpswrd" + num
                userid = "DU" + str(random.randint(1000,9999))



            # Process the form data as needed
            # Create a new User instance and add it to the database
            new_user = Users(
                username=username,
                email=email,  # Assuming Email is used as an example for account_user_name
                password=password,
                userid=userid,
                admin=False,
            )

            db.session.add(new_user)
            db.session.commit()

            # Log the new user information
            app.logger.info(f"New User: {str(new_user)}")

            # Redirect to the /confirmation route with data as query parameters
            return redirect(url_for('confirmation', user_id=new_user.userid))

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
    user_id = session['user_id']
    logging.info(user_id)
    return render_template('/home.html')

if __name__ == '__main__':
    app.run()
