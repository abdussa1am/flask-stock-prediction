from flask import Flask , render_template , request , jsonify
from flask import make_response , redirect , url_for , flash
from flask_bootstrap import Bootstrap
import requests
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm , sign
import os
import psycopg2
import json
from flask_mail import Mail, Message


app = Flask(__name__)
bootstrap = Bootstrap(app)
#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#app.config.from_object('config.DevelopmentConfig')
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:karachiking@localhost:5432/ajd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdussalam11051998@gmail.com'
app.config['MAIL_PASSWORD'] = 'karachiking11051998'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)
class Signin(db.Model):
        __tablename__ = 'signin'
        id = db.Column(db.Integer, primary_key = True)
        email = db.Column(db.String(60), unique=True)
        name = db.Column(db.String(80), nullable=False)
db.create_all()

@app.route('/') 
def index():
    msg = Message( 
                'Hello', 
                 sender ='abdussalam11051998@gmail.com', 
                 recipients = ['abdussalam11051998@gmail.com'] 
                )  
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg) 
    return 'Sent'
@app.route("/chart" , methods=('GET', 'POST'))
def chart():
    res = requests.get('https://fcsapi.com/api-v2/stock/history?id=1&period=1d&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    ope = [i+2['o'] for i in data['response']] 
    dte = [i['tm'] for i in data['response']]
    return render_template('chart.html', oneday=ope ,dte=dte)
@app.route('/hello')
def hello():
    res = requests.get('https://fcsapi.com/api-v2/stock/list?country=Pakistan&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    sto = [i['stock_id'] for i in data['response']]
    ads =  ', '.join(sto)
    res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(ads)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    lat = res.json()
    rest = requests.get('https://fcsapi.com/api-v2/stock/profile?id='+str(ads)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    comp = rest.json()
    #op = [j['price'] for j in lat['response']]
    return render_template('hello.html' ,  data = data , lat = lat , comp=comp)
@app.route('/api/<int:name>') 
def api(name):
    res= requests.get('https://fcsapi.com/api-v2/stock/performance?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    per = res.json()
    reste = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = reste.json()
    #res = requests.get('https://fcsapi.com/api-v2/stock/history?id='+str(name)+'&period=1d&from=2020-4-01&to=2020-06-20&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    #grph = res.json()
    rest = requests.get('https://fcsapi.com/api-v2/stock/profile?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    comp = rest.json()
    fun = requests.get('https://fcsapi.com/api-v2/stock/technicals?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    fund = fun.json()
    #ope = [i['o'] for i in grph['response']] 
    #dte = [j['tm'] for j in grph['response']]
    #return render_template('chart.html', values=values, labels=labels , oneday=ope ,dte=dte)
    return render_template('err.html' , data=data  , comp=comp , per=per , fund = fund)  
    #, per=per,  dte=dte , oneday=ope 
   
@app.route('/err')
def err():
    return render_template('err.html') 
@app.route('/signin' , methods=('GET', 'POST'))
def signin():
    form = sign()
    if request.method =='POST' and form.validate_on_submit():
        nem = Signin.query.filter_by(email= form.email.data).first()
        if nem:
            flash("asddsakn")
            return redirect(url_for('user'))
    return render_template('signin.html' , form= form)
@app.route('/user')
def user():
    res = requests.get('https://fcsapi.com/api-v2/stock/list?country=pakistan&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    return render_template('user.html', data= data )
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = ContactForm()
    if request.method =='POST' and form.validate_on_submit():
        users = Signin(name = form.name.data ,email = form.email.data)
        db.session.add(users)
        db.session.commit()
        flash("Registered succesfull")
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)
if __name__ == '__main__':
    app.run(debug=True, port=33507)
