from flask import Flask , render_template , request , jsonify
from flask import make_response , redirect , url_for , flash
from flask_bootstrap import Bootstrap
import requests
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm , sign
import os
import psycopg2
app = Flask(__name__)
bootstrap = Bootstrap(app)
#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.from_object('config.DevelopmentConfig')
app.config['SECRET_KEY'] = 'any secret string'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:karachiking@localhost:5432/ajd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
class Signin(db.Model):
        __tablename__ = 'signin'
        id = db.Column(db.Integer, primary_key = True)
        email = db.Column(db.String(60), unique=True)
        name = db.Column(db.String(80), nullable=False)
db.create_all()

@app.route('/') 
def index():
    return 'sdf'
@app.route('/hello')
def hello():
    res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    return render_template('hello.html')
@app.route('/api/<int:name>') 
def api(name):
    res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    return render_template('err.html' , data= data)
@app.route('/err')
def err():
    return render_template('err.html') 
@app.route('/signin' , methods=('GET', 'POST'))
def signin():
    form = sign()
    if request.method =='POST' and form.validate_on_submit():
        nem = Signin.query.filter_by(email= form.email.data).first()
        if nem:
            return redirect(url_for('user'))
    return render_template('signin.html' , form= form)
@app.route('/user')
def user():
    res = requests.get('https://fcsapi.com/api-v2/stock/list?country=pakistan&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU&fbclid=IwAR1_XLTMSH3mKhd8uaTpXKtVQRsPS-EwNtWdlu4oM0f8fE2G9i5K2mPKcTw')
    data = res.json()
    return render_template('user.html', data= data)
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = ContactForm()
    if request.method =='POST' and form.validate_on_submit():
        users = Signin(name = form.name.data ,email = form.email.data)
        db.session.add(users)
        db.session.commit()
        #peter = Contact.query.filter_by(name = ne).first()
        #flash(names)
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)
if __name__ == '__main__':
    app.run(debug=True, port=33507)
