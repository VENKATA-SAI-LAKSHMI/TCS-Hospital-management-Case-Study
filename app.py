from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect
)
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
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
    error = ''
    return render_template('home.html')


@app.route('/login1', methods=['GET', 'POST'])
def login1():
    message = 'Welcome Registration/Admission desk executive'
    error = ''
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i in cur.execute('SELECT * FROM Login'):
            if i[0] == username and i[1] == password:
                return redirect(url_for('profile1'))
        return render_template('login.html', z=message, error='Error: Incorrect Username or Password')
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
    return render_template('profile1.html')


@app.route('/createpatient', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        sid = request.form['cid']
        id = int(sid)+1
        name = request.form['name']
        age = request.form['age']
        doa = request.form['date']
        tob = request.form['trans']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        status = "created"

        con = sql.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("INSERT INTO patients (sid,id,name,age,doa,tob,address,city,state,status) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (sid, id, name, age, doa, tob, address, city, state, status))
        con.commit()
        con.close()

    return render_template('createpatient.html')


@app.route('/updatepatient', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = request.form['sid']
            print(55)
            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row

            cur = con.cursor()
            ss = "SELECT * FROM patients WHERE SID=?;"
            for row in cur.execute(ss, [getsid]):
                sid = row[0]
                name = row[2]
                age = row[3]
                doa = row[4]
                tob = row[5]
                address = row[6]
                city = row[7]
                state = row[8]

            return render_template("updatepatient.html", sid=sid, tob=tob, name=name, age=age, doa=doa, address=address, city=city, state=state)
        if "sub" in request.form:
            sid = request.form['getsid']
            id = int(sid)+1
            name = request.form['name']
            age = request.form['age']
            doa = request.form['doa']
            tob = request.form.get('tob')
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            status = "created"

            con = sql.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute("UPDATE patients SET id=?,name=?,age=?,doa=?,tob=?,address=?,city=?,state=?,status=? WHERE sid=?",
                        (id, name, age, doa, tob, address, city, state, status, sid))
            con.commit()
            con.close()
            return render_template('searchud.html', z='Updated Sucessfully')

    return render_template('searchud.html')


@app.route('/deletepatient', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = request.form['sid']
            print(55)
            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row
            cur = con.cursor()
            ss = "SELECT * FROM patients WHERE SID=?;"
            if len(ss) == 35:
                return render_template('searchud.html', z='No Data Found')
            for row in cur.execute(ss, [getsid]):
                sid = row[0]
                name = row[2]
                age = row[3]
                doa = row[4]
                tob = row[5]
                address = row[6]
                city = row[7]
                state = row[8]

            return render_template("deletepatient.html", sid=sid, tob=tob, name=name, age=age, doa=doa, address=address, city=city, state=state)

        sid = request.form['getsid']
        con = sql.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("DELETE  FROM patients WHERE sid=?;", [sid])
        con.commit()
        con.close()
        print(44)
    return render_template('searchud.html')


@app.route('/searchpatients', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = request.form['sid']
            print(55)
            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row
            cur = con.cursor()
            count = 0
            l = []
            ss = "SELECT * FROM patients WHERE SID=?;"
            for row in cur.execute(ss, [getsid]):
                l.append(row)
                count += 1

            if count == 0:
                return render_template('searchud.html', z='No Data Found')
            return render_template("searchresults.html", z=l )
    return render_template('searchud.html')

@app.route('/viewpatients')
def viewall():
    l = []
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM patients'):
        l.append(row)
    return render_template('searchresults.html',z=l)


@app.route('/patientbill')
def patientbill():
    return render_template('patientbill.html')


if __name__ == '__main__':
    app.run(debug=True)
