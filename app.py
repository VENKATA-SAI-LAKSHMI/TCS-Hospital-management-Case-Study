from flask import (
    Flask,
    render_template,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


class Patients(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    doa = db.Column(db.DateTime)
    tob = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    meds = db.relationship('Medicines', backref='patients')


diag_meds = db.Table('diag_meds',
                     db.Column('med_id', db.Integer, db.ForeignKey(
                         'medicines.id'), primary_key=True),
                     db.Column('diagn_id', db.Integer, db.ForeignKey(
                         'diagnostics.id'), primary_key=True)
                     )


class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(50), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

    diagn = db.relationship('Diagnostics', secondary=diag_meds)


class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagn = db.Column(db.String(500), nullable=False)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login1')
def login1():
    message = 'Welcome Registration/Admission desk executive'
    return render_template('login.html', z=message)


@app.route('/login2')
def login2():
    message = 'Welcome Pharmacist'
    return render_template('login.html', z=message)


@app.route('/login3')
def login3():
    message = 'Welcome Diagnostic services executive'
    return render_template('login.html', z=message)

@app.route('/profile1')
def profile1():
    message = 'Welcome Diagnostic services executive'
    return render_template('profile1.html', z=message)

@app.route('/createpatient')
def create():
    message = 'Welcome Diagnostic services executive'
    return render_template('createpatient.html')


if __name__ == '__main__':
    app.run(debug=True)
