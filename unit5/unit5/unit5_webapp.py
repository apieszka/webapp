from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
from sqlalchemy import func
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

class Odpowiedzi_wiedza_dydaktyczna(db.Model):
    __tablename__ = 'Odpowiedzi_wiedza_dydaktyczna'

    id_kandydata = db.Column(db.Integer, primary_key=True)
    p1 = db.Column(db.SmallInteger)
    p2 = db.Column(db.SmallInteger)
    p3 = db.Column(db.SmallInteger)
    p4 = db.Column(db.SmallInteger)
    p5 = db.Column(db.SmallInteger)
    p6 = db.Column(db.SmallInteger)
    p7 = db.Column(db.SmallInteger)
    p8 = db.Column(db.SmallInteger)
    p9 = db.Column(db.SmallInteger)
    p10 = db.Column(db.SmallInteger)
    p11 = db.Column(db.SmallInteger)
    p12 = db.Column(db.SmallInteger)
    p13 = db.Column(db.SmallInteger)
    p14 = db.Column(db.SmallInteger)
    p15 = db.Column(db.SmallInteger)
    p16 = db.Column(db.SmallInteger)
    p17 = db.Column(db.SmallInteger)
    p18 = db.Column(db.SmallInteger)

    def __init__(self, id_kandydata, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18):
        self.id_kandydata = id_kandydata
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9
        self.p10 = p10
        self.p11 = p11
        self.p12 = p12
        self.p13 = p13
        self.p14 = p14
        self.p15 = p15
        self.p16 = p16
        self.p17 = p17
        self.p18 = p18

class Odpowiedzi_umiejętności_miękkie(db.Model):
    __tablename__ = 'Odpowiedzi_umiejętności_miękkie'

    id_kandydata = db.Column(db.Integer, primary_key=True)
    p1 = db.Column(db.SmallInteger)
    p2 = db.Column(db.SmallInteger)
    p3 = db.Column(db.SmallInteger)
    p4 = db.Column(db.SmallInteger)
    p5 = db.Column(db.SmallInteger)
    p6 = db.Column(db.SmallInteger)
    p7 = db.Column(db.SmallInteger)
    p8 = db.Column(db.SmallInteger)
    p9 = db.Column(db.SmallInteger)
    p10 = db.Column(db.SmallInteger)
    p11 = db.Column(db.SmallInteger)
    p12 = db.Column(db.SmallInteger)

    def __init__(self, id_kandydata, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12):
        self.id_kandydata = id_kandydata
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9
        self.p10 = p10
        self.p11 = p11
        self.p12 = p12

class Kandydaci(db.Model):
    __tablename__ = 'Kandydaci'
    id_kandydata = db.Column(db.Integer, primary_key=True)
    wiek = db.Column(db.String(15))
    płeć = db.Column(db.String(20))
    adres_email = db.Column(db.String(100))
    poziom_wykształcenia = db.Column(db.String(25))
    id_uczelni = db.Column(db.Integer)
    id_obszaru = db.Column(db.Integer)
    sytuacja_zawodowa = db.Column(db.String(20))
    id_wojewodztwa = db.Column(db.Integer)
    data_dodania = db.Column(db.TIMESTAMP, default=db.func.now())

    def __init__(self, id_kandydata, wiek, płeć, adres_email, poziom_wykształcenia, id_uczelni, id_obszaru, sytuacja_zawodowa, id_wojewodztwa):
        self.id_kandydata = id_kandydata
        self.wiek = wiek
        self.płeć = płeć
        self.adres_email = adres_email
        self.poziom_wykształcenia = poziom_wykształcenia
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
    max_id = db.session.query(func.max(Kandydaci.id_kandydata)).scalar()

    id_kandydata = max_id + 1
    wiek = request.form.get('wiek')
    płeć = request.form.get('płeć')
    adres_email = request.form.get('email')
    poziom_wykształcenia = request.form.get('poziom')
    id_uczelni = request.form.get('uczelnia')
    id_obszaru = request.form.get('obszar')
    sytuacja_zawodowa = request.form.get('work')
    id_wojewodztwa = request.form.get('woj')

    # Save the data
    k = Kandydaci(id_kandydata, wiek, płeć, adres_email, poziom_wykształcenia, id_uczelni, id_obszaru, sytuacja_zawodowa, id_wojewodztwa)
    db.session.add(k)
    db.session.commit()

    owd_p1 = request.form.get('question1')
    owd_p2 = request.form.get('question2')
    owd_p3 = request.form.get('question3')
    owd_p4 = request.form.get('question4')
    owd_p5 = request.form.get('question5')
    owd_p6 = request.form.get('question6')
    owd_p7 = request.form.get('question7')
    owd_p8 = request.form.get('question8')
    owd_p9 = request.form.get('question9')
    owd_p10 = request.form.get('question10')
    owd_p11 = request.form.get('question11')
    owd_p12 = request.form.get('question12')
    owd_p13 = request.form.get('question13')
    owd_p14 = request.form.get('question14')
    owd_p15 = request.form.get('question15')
    owd_p16 = request.form.get('question16')
    owd_p17 = request.form.get('question17')
    owd_p18 = request.form.get('question18')

    owd_points = 0
    for p in [owd_p1, owd_p2, owd_p3, owd_p4, owd_p5, owd_p6, owd_p7, owd_p8,
                                        owd_p9, owd_p10, owd_p11, owd_p12, owd_p13, owd_p14, owd_p15, owd_p16, owd_p17, owd_p18]:
        owd_points = owd_points + int(p)


    owd = Odpowiedzi_wiedza_dydaktyczna(id_kandydata, owd_p1, owd_p2, owd_p3, owd_p4, owd_p5, owd_p6, owd_p7, owd_p8,
                                        owd_p9, owd_p10, owd_p11, owd_p12, owd_p13, owd_p14, owd_p15, owd_p16, owd_p17, owd_p18)
    db.session.add(owd)
    db.session.commit()

    oum_p1 = request.form.get('question1m')
    oum_p2 = request.form.get('question2m')
    oum_p3 = request.form.get('question3m')
    oum_p4 = request.form.get('question4m')
    oum_p5 = request.form.get('question5m')
    oum_p6 = request.form.get('question6m')
    oum_p7 = request.form.get('question7m')
    oum_p8 = request.form.get('question8m')
    oum_p9 = request.form.get('question9m')
    oum_p10 = request.form.get('question10m')
    oum_p11 = request.form.get('question11m')
    oum_p12 = request.form.get('question12m')

    oum_points = 0
    for p in [oum_p1, oum_p2, oum_p3, oum_p4, oum_p5, oum_p6, oum_p7, oum_p8,
                                        oum_p9, oum_p10, oum_p11, oum_p12]:
        oum_points = oum_points + int(p)

    oum = Odpowiedzi_umiejętności_miękkie(id_kandydata, oum_p1, oum_p2, oum_p3, oum_p4, oum_p5, oum_p6, oum_p7, oum_p8,
                                        oum_p9, oum_p10, oum_p11, oum_p12)
    db.session.add(oum)
    db.session.commit()

    return render_template('thankyou.html', owd_points=owd_points, oum_points=oum_points)


if __name__ == "__main__":
    app.debug = True
    app.run()
