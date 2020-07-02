from flask import Flask , render_template , request , jsonify , Blueprint
from flask import make_response , redirect , url_for , flash
from flask_bootstrap import Bootstrap
import requests
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm , sign
import os
import psycopg2
import json
from flask_mail import Mail, Message
from flask_login import LoginManager,  UserMixin ,logout_user, current_user, login_user

from flask_login import login_required

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
#app.config.from_object('config.ProductionConfig')
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:karachiking@localhost:5432/ajd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'engr.abdussalam98@gmail.com'
app.config['MAIL_PASSWORD'] = 'karachiking11051998'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)
class Signin( UserMixin,db.Model):
        __tablename__ = 'signin'
        id = db.Column(db.Integer, primary_key = True)
        email = db.Column(db.String(60), unique=True)
        name = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(id):
    return Signin.query.get(int(id))
db.create_all()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(requests.exceptions.ConnectionError)
def handle_bad_request(e):
    return '<h1>check your internet or try again after 1 minute</h1>', 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
    
@app.route("/chart")
def chart():
    return render_template('chart.html')
@app.route('/hello')
def hello():
    res = requests.get('https://fcsapi.com/api-v2/stock/list?country=Pakistan&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    sto = [i['stock_id'] for i in data['response']]
    ads =  ', '.join(sto)
    res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(ads)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    lat = res.json()
    return render_template('hello.html' ,  data = data , lat = lat)
@app.route('/profile/<int:name>') 
def api(name):
    res = requests.get('https://fcsapi.com/api-v2/stock/history?id='+str(name)+'&period=1d&from=2020-05-28&to=2020-06-27&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    grph = res.json()
    ope = [i['o'] for i in grph['response']] 
    dte = [j['tm'] for j in grph['response']]
    rest = requests.get('https://fcsapi.com/api-v2/stock/profile?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    compan = rest.json()
    res = requests.get('https://fcsapi.com/api-v2/stock/performance?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    per = res.json()
    #res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    #data = res.json()
    return render_template('err.html' , per=per, company=compan, dte=dte , oneday=ope)
    #fun = requests.get('https://fcsapi.com/api-v2/stock/technicals?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    #funds = fun.json()
@app.route('/analysis/<int:name>') 
def analysis(name):
    res = requests.get('https://fcsapi.com/api-v2/stock/history?id='+str(name)+'&period=1w&from=2019-06-30&to=2020-06-30&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    grph = res.json()
    openy = [i['o'] for i in grph['response']] 
    dtey = [j['tm'] for j in grph['response']]
    res = requests.get('https://fcsapi.com/api-v2/stock/history?id='+str(name)+'&period=1d&from=2020-05-30&to=2020-06-30&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    grph = res.json()
    ope = [i['o'] for i in grph['response']] 
    dte = [j['tm'] for j in grph['response']]
    fun = requests.get('https://fcsapi.com/api-v2/stock/technicals?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    fund = fun.json()
    return render_template('profile.html' , dte=dte , oneday=ope , openy=openy , dtey=dtey , fund=fund)
@app.route('/err')
def err():
    return render_template('err.html') 
@app.route('/signin' , methods=('GET', 'POST'))
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = sign()
    if request.method =='POST' and form.validate_on_submit():
        nem = Signin.query.filter_by(email= form.email.data).first()
        if nem is None:
            flash("invalid username or password")
            return redirect(url_for('signin'))
        login_user(nem)
        msg = Message( 
                'Hi {{nem.name}}', 
                 sender ='engr.abdussalam98@gmail.com', 
                 recipients = [nem.email] 
               )  
        msg.body = '<h1>Thanks for visiting website  !!<h1>'
        msg.html = "<h4>Thanks for visiting psx-flask-stock</h4><p>In Psx-flask-stock you can easily analyze pakistan stock market and predict prices </p><br><br><h4>Regards, <br>Abdus Salam</h4>"
        mail.send(msg) 
        return redirect(url_for('hello'))
    return render_template('signin.html' , form= form)
@app.route('/user')
def user():
    res = requests.get('https://fcsapi.com/api-v2/stock/list?country=pakistan&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    return render_template('user.html', data= data)
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = ContactForm()
    if request.method =='POST' and form.validate_on_submit():
        using = Signin(name = form.name.data ,email = form.email.data)
        db.session.add(using)
        db.session.commit()
        #login_user(users)
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signin'))
if __name__ == '__main__':
    app.run(debug=True, port=33507)
