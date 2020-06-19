import os

from flask import Flask, render_template, url_for, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import SignUpForm
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ygieszkwjoenfbmwkxvd'


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template('BarberShop.html')


@app.route("/signup", methods= ['POST','GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for(index))
    return render_template('signup.html', title='SignUp fella',form=form)



@app.route("/login", methods= ['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('/'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='SignUp fella',form=form)



if __name__ == '__main__':
    app.run(debug=True)
