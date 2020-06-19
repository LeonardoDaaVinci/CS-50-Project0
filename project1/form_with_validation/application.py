import os

from flask import Flask, render_template, url_for, flash, redirect, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import SignUpForm
from forms import LoginForm, SearchBarForm, BookDisplayForm

from flask_toastr import Toastr


app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.raw_connection()
cursor = connection.cursor()
db = scoped_session(sessionmaker(bind=engine))
app.config['SECRET_KEY'] = 'ygieszkwjoenfbmwkxvd'
toastr = Toastr(app)

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
    global nameOfTheUser
    nameOfTheUser =''
    return render_template('HomePage.html')

@app.route("/signup", methods= ['POST','GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        db.execute("INSERT INTO userInfo (userName, password, emailId) VALUES (:userName, :password, :emailId)", 
                            {"userName": form.username.data,"password":form.password.data,"emailId":form.email.data})
        db.commit()
        nameOfTheUser= info.username
        return redirect(url_for('bookPage'))
        #return flash(f'Account created for {form.username.data}!', 'success')
        # return redirect(url_for('index'))
    return render_template('signup.html', title='SignUp fella',form=form)

@app.route("/login", methods= ['POST','GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        info = db.execute("SELECT * FROM userInfo WHERE emailid= :id",{"id":form.email.data}).fetchone()
        pwd = request.form.get("password")
        if (info.password == pwd):
            # flash(f'Account created with {form.email.data}!', 'success')
            form = SearchBarForm()
            nameOfTheUser= info.username
            return redirect(url_for('bookPage'))
        else :
            flash('Invalid Credentials')
            return render_template('login.html', title='Sign in fella',form=form)
    else:
        return render_template('login.html', title='Sign in fella',form=form)

@app.route("/bookPage", methods= ['POST','GET'])
def bookPage():
    form = SearchBarForm()
    if request.method == 'POST':
        name=request.form['searchFor']
        pattern = "%"+name+"%"
        usrName =nameOfTheUser 
        booksList =db.execute("SELECT * FROM bookInfo WHERE isbn LIKE :s OR title LIKE :s OR author LIKE :s", {"s":pattern}).fetchall()
        return render_template('bookList.html',booksList =booksList,usrName =nameOfTheUser )
    else:
        return render_template('bookSearch.html',form=form,usrName=nameOfTheUser)

@app.route("/bookList", methods= ['POST','GET'])
def bookList():
    usrName =nameOfTheUser 
    return render_template('bookList.html',usrName=nameOfTheUser)

@app.route("/bookDisplay", methods= ['POST','GET'])
def bookDisplay():
    form = BookDisplayForm()
    book=request.args.get('book')
    bookInfo = db.execute("SELECT * FROM bookInfo WHERE title = :title",{"title":book }).fetchone()
    reviewList = db.execute("SELECT textReview FROM reviews WHERE bookId = :bookId",{"bookId":bookInfo.id }).fetchall()
    ident =  db.execute("SELECT * FROM userInfo WHERE userName = :userName",{"userName":nameOfTheUser }).fetchone()
    usrName =nameOfTheUser 
    ii = ident.userid
    if request.method == 'POST':
        review=request.form['body']
        db.execute("INSERT INTO reviews (textReview, bookId, reviewerId) VALUES (:textReview, :bookId, :reviewerId)", 
                        {"textReview": review,"bookId":bookInfo.id,"reviewerId":ii} )
        db.commit()
        reviewList = db.execute("SELECT textReview FROM reviews WHERE bookId = :bookId",{"bookId":bookInfo.id }).fetchall()
        return render_template('bookDisplay.html',form=form,bookInfo= bookInfo,reviewList=reviewList,usrName=nameOfTheUser)
    else:
        return render_template('bookDisplay.html',form=form,bookInfo= bookInfo,reviewList=reviewList,usrName=nameOfTheUser)

if __name__ == '__main__':
    app.run()
