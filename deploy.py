from flask import Flask , render_template , request , jsonify
from flask import make_response , redirect , url_for , flash
from flask_bootstrap import Bootstrap
import requests
from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
import psycopg2
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:karachiking@localhost:5432/ajd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class Contact(db.Model):
        __tablename__ = 'mynu'
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(80), nullable=False)
db.create_all()
class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        DataRequired()])

    submit = SubmitField('Submit')
@app.route('/') 
def index():
    return render_template("err.html")
@app.route('/hello')
def hello():
    res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    return render_template('hello.html', data= data)
@app.route('/api/<int:name>') 
def api(name):
    res = requests.get('https://fcsapi.com/api-v2/stock/latest?id='+str(name)+'&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU')
    data = res.json()
    return render_template('err.html' , data= data)
@app.route('/err')
def err():
    return render_template('err.html') 
def base():
    return render_template('base.html')
@app.route('/user')
def user():
    res = requests.get('https://fcsapi.com/api-v2/stock/list?country=pakistan&access_key=YON9guMpjGdHapymnGbCOpBOvAtIMbsINqH866bXpgOvxHavTU&fbclid=IwAR1_XLTMSH3mKhd8uaTpXKtVQRsPS-EwNtWdlu4oM0f8fE2G9i5K2mPKcTw')
    data = res.json()
    return render_template('user.html', data= data)
@app.route('/signin', methods=('GET', 'POST'))
def signin():
    form = ContactForm()
    if request.method =='POST' and form.validate_on_submit(): 
        users = Contact(name = form.name.data)
        db.session.add(users)
        db.session.commit()
        peter = Contact.query.filter_by(name='sad').first()
        names = peter.name
        flash(names)
        return redirect(url_for('err'))
    return render_template('signin.html', form=form)
if __name__ == '__main__':
    app.run(debug=True)
