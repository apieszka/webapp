from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
import os


app = Flask(__name__, static_url_path='/static')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://schneid2:C3sF3RzTsmtnpdJY@mysql.agh.edu.pl:3306/schneid2'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Uczelnie(db.Model):
    __tablename__ = 'Uczelnie'

    id_uczelni = db.Column(db.Integer, primary_key=True)
    nazwa_uczelni = db.Column(db.String(100))

    def __init__(self, id_uczelni, nazwa_uczelni):
        self.id_uczelni = id_uczelni
        self.nazwa_uczelni = nazwa_uczelni

class Wojewodztwa(db.Model):
    __tablename__ = 'Wojewodztwa'

    id_wojewodztwa = db.Column(db.Integer, primary_key=True)
    nazwa_wojewodztwa = db.Column(db.String(25))

    def __init__(self, id_wojewodztwa, nazwa_wojewodztwa):
        self.id_wojewodztwa = id_wojewodztwa
        self.nazwa_wojewodztwa = nazwa_wojewodztwa

class Obszary_tematyczne(db.Model):
    __tablename__ = 'Obszary_tematyczne'

    id_obszaru = db.Column(db.Integer, primary_key=True)
    nazwa_obszaru = db.Column(db.String(25))

    def __init__(self, id_obszaru, nazwa_obszaru):
        self.id_obszaru = id_obszaru
        self.nazwa_obszaru = nazwa_obszaru

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=50))
    age = db.Column(db.Integer)
    income = db.Column(db.Integer)
    satisfaction = db.Column(db.Integer)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)

    def __init__(self, firstname, email, age, income, satisfaction, q1, q2):
        self.firstname = firstname
        self.email = email
        self.age = age
        self.income = income
        self.satisfaction = satisfaction
        self.q1 = q1
        self.q2 = q2

class Kandydaci(db.Model):
    __tablename__ = 'Kandydaci'
    id_kandydata = db.Column(db.Integer, primary_key=True)
    wiek = db.Column(db.String(15))
    płeć = db.Column(db.String(20))
    adres_email = db.Column(db.String(100))
    poziom_wyksztalcenia = db.Column(db.String(25))
    id_uczelni = db.Column(db.Integer)
    id_obszaru = db.Column(db.Integer)
    sytuacja_zawodowa = db.Column(db.String(20))
    id_wojewodztwa = db.Column(db.Integer)
    data_dodania = db.Column(db.TIMESTAMP, default=db.func.now())

    def __init__(self, id_kandydata, wiek, adres_email, poziom_wyksztalcenia, id_uczelni, id_obszaru, sytuacja_zawodowa, id_wojewodztwa):
        self.id_kandydata = id_kandydata
        self.wiek = wiek
        self.adres_email = adres_email
        self.poziom_wyksztalcenia = poziom_wyksztalcenia
        self.id_uczelni = id_uczelni
        self.id_obszaru = id_obszaru
        self.sytuacja_zawodowa = sytuacja_zawodowa
        self.id_wojewodztwa = id_wojewodztwa

db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    lista_wojewodztw = db.session.query(Wojewodztwa).all()
    lista_uczelni = db.session.query(Uczelnie).all()
    lista_obszarow = db.session.query(Obszary_tematyczne).all()
    return render_template('form.html', lista_uczelni=lista_uczelni, lista_wojewodztw=lista_wojewodztw, lista_obszarow=lista_obszarow)

@app.route("/krok")
def show_krok():
    return render_template('krok.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)

# @app.route("/raw")
# def show_raw():
#     fd = db.session.query(Formdata).all()
#     return render_template('raw.html', formdata=fd)

@app.route("/faq")
def show_faq():
    # fd = db.session.query(Formdata).all()
    return render_template('faq.html')

@app.route("/test")
def show_test():
    return render_template('form_test.html')

@app.route("/result")
def show_result():
    fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
    satisfaction = []
    q1 = []
    q2 = []
    for el in fd_list:
        satisfaction.append(int(el.satisfaction))
        q1.append(int(el.q1))
        q2.append(int(el.q2))

    if len(satisfaction) > 0:
        mean_satisfaction = statistics.mean(satisfaction)
    else:
        mean_satisfaction = 0

    if len(q1) > 0:
        mean_q1 = statistics.mean(q1)
    else:
        mean_q1 = 0

    if len(q2) > 0:
        mean_q2 = statistics.mean(q2)
    else:
        mean_q2 = 0

    # Prepare data for google charts
    data = [['Satisfaction', mean_satisfaction], ['Python skill', mean_q1], ['Flask skill', mean_q2]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    max_id = session.query(func.max(Kandydaci.id_kandydata)).scalar()

    id_kandydata = max_id + 1
    wiek = request.form.get('wiek')
    płeć = request.form.get('płeć')
    adres_email = request.form.get('email')
    poziom_wyksztalcenia = request.form.get('poziom')
    id_uczelni = request.form.get('uczelnia')
    id_obszaru = request.form.get('obszar')
    sytuacja_zawodowa = request.form.get('work')
    id_wojewodztwa = request.form.get('woj')

    # Save the data
    fd = Kandydaci(id_kandydata, wiek, płeć, adres_email, poziom_wyksztalcenia, id_uczelni, id_obszaru, sytuacja_zawodowa, id_wojewodztwa)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
