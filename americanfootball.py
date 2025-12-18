'''Import these modules to use them. In particular the datetime, the
flask, etc.'''
import datetime
import logging
import socket
from flask import Flask, render_template, request, redirect, url_for, session

# flask --app americanfootball run

# Name: Alexander Sheidu
# Course: SDEV 300/6381
# Date: March 1, 2024

'''In this python app, I am making a website based on American Football, 
the rules, how to play, and I am using html with python code, to make the
website. The website has different pages, which can be accessed through
each page. I will be making a user registration, and a login for the user
to enter the website. I will also, be making a logout button, for the 
Index, News, or Super Bowl page for once the user is logged in. As well as
a user password update form.'''

# Initialize the name of the Flask
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'


@app.route("/")
def start():
    '''This function redirects to the user registration page.'''
    return redirect(url_for('registration'))

# Modify other routes to check if the user is logged in or registered


@app.route("/index")
def index():
    '''Go to this page in the URL, for information on American Football
    facts.'''
    if 'username' not in session or 'email' not in session:
        # Redirect to login if user is not logged in
        return redirect(url_for('login'))
    return render_template('index.html', dt=datetime.datetime.now())


@app.route("/news")
def news():
    '''Go to this page in the URL, for information on American Football
    News, from different leagues.'''
    if 'username' not in session or 'email' not in session:
        # Redirect to login if user is not logged in
        return redirect(url_for('login'))
    return render_template('news.html', dt=datetime.datetime.now())


@app.route("/superbowl")
def superbowl():
    '''Go to this page in the URL, for information on American Football's
    Super Bowl, the history, facts and stats.'''
    if 'username' not in session or 'email' not in session:
        # Redirect to login if user is not logged in
        return redirect(url_for('login'))
    return render_template('superbowl.html', dt=datetime.datetime.now())


# Initialize database for user registration
registered_users = []

# Common passwords
passwords = []


@app.route("/registration", methods=["GET", "POST"])
def registration():
    '''This is the registration page, where the user enters their
    full name, username, email and password.'''
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Perform password complexity check
        if (len(password) < 12 or not any(char.isupper() for char in password) or
            not any(char.islower() for char in password)
            or not any(char.isdigit() for char in password) or
                not any(char in "!@#$%^&*()-_=+{}[]|;:'\",.<>?`~" for char in password)):
            return render_template('registration.html', dt=datetime.datetime.now())

        # Check if username already exists
        for user in registered_users:
            if user["username"] == username:
                return render_template('registration.html', dt=datetime.datetime.now())

            if user["email"] == email:
                return render_template('registration.html', dt=datetime.datetime.now())

        # Register user
        registered_users.append(
            {"username": username, "email": email, "password": password})

        # Set session variables upon successful registration
        session['username'] = request.form.get("username")
        session['email'] = request.form.get("email")

        return redirect(url_for('login'))

    return render_template('registration.html', dt=datetime.datetime.now())


@app.route("/update", methods=["GET", "POST"])
def update():
    '''This function updates the password, the user enters their username
    and then their desired password.'''
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Perform password complexity check
        if (len(password) < 12 or not any(char.isupper() for char in password) or
            not any(char.islower() for char in password)
            or not any(char.isdigit() for char in password) or
                not any(char in "!@#$%^&*()-_=+{}[]|;:'\",.<>?`~" for char in password)):
            return render_template('updatepassword.html', msg="Password failed complexity"
                                   " test, please select a different password", dt=datetime.datetime.now())

        # Check if username already exists
        for user in registered_users:
            if user["username"] == username:
                # Check if the password matches the previous password
                if user["password"] == password:
                    return render_template('updatepassword.html', msg="The same password as"
                                           " your previous password, please select a different password",
                                           dt=datetime.datetime.now())
                # Check if the password is in common passwords
                if password in passwords:
                    return render_template('updatepassword.html', msg="Password is in common"
                                           " passwords, please select a different password",
                                           dt=datetime.datetime.now())

                # Register the new password for the user
                user["password"] = password
                return redirect(url_for('login'))

    return render_template('updatepassword.html', dt=datetime.datetime.now())


@app.route("/login", methods=["GET", "POST"])
def login():
    '''This is the login page, where the user enters their
    username and password.'''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Extract the selected page from the form
        selected_page = request.form.get("page")

        # Check if user exists and password matches (mock implementation)
        for user in registered_users:
            if user["username"] == username and user["password"] == password:
                # Set session variables upon successful login
                session['username'] = username
                session['email'] = user['email']

                # Redirect to the selected page after successful login
                if selected_page == "index":
                    return redirect(url_for('index'))
                elif selected_page == "news":
                    return redirect(url_for('news'))
                elif selected_page == "superbowl":
                    return redirect(url_for('superbowl'))

        hostname = socket.gethostname()
        client_ip = socket.gethostbyname(hostname)
        logging.basicConfig(filename='af.log', filemode='a',
                            format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.warning(client_ip + ' - failed log in ')

        return render_template('login.html', dt=datetime.datetime.now())

    return render_template('login.html', dt=datetime.datetime.now())


@app.route("/logout", methods=["GET", "POST"])
def logout():
    '''This logs out of the Index, News, or Super Bowl pages.'''
    # Clear session variables upon logout
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))


def load(fname):
    '''This loads the common passwords, and allocates it 
    to the list.'''
    file = open(fname, "r")
    lines = file.read().split("\n")
    for password in lines:
        passwords.append(password.strip())


# In order to run the program
if __name__ == '__main__':
    app.run(debug=True)
