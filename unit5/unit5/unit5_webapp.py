from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics


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



db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    lista_uczelni = db.session.query(Uczelnie).all() # [(uczelnie.id_uczelni, uczelnie.nazwa_uczelni) for uczelnia in Uczelnie.query.all()]
    return render_template('form.html', lista_uczelni=lista_uczelni)

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
    # Get data from FORM
    firstname = request.form.get('firstname')
    email = request.form.get('email')
    age = request.form.get('age')
    income = request.form.get('income')
    satisfaction = request.form.get('satisfaction')
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')

    # Save the data
    fd = Formdata(firstname, email, age, income, satisfaction, q1, q2)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
