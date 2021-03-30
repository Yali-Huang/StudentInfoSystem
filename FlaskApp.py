from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./data.db"  # local database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True


app = Flask(__name__)
app.secret_key = b'_5#ya2L"F4Q8z\n\xec]/'
app.config.from_object(Config)
db = SQLAlchemy(app)
# define the student model


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(32), unique=False)
    last_name = db.Column(db.String(32), unique=False)
    dob = db.Column(db.String(32), unique=False)
    amount_due = db.Column(db.Float(), unique=False)


# create db from model
db.create_all()
db.session.commit()


@app.route('/')
def index():
    return redirect(url_for('query_all'))
    # return render_template('index.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        #student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        amount_due = request.form['amount_due']

        try:
            print(f'{first_name}, {last_name}, {dob},{amount_due}')
            new_student = Student(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                amount_due=amount_due)
            db.session.add(new_student)
            db.session.commit()
            # return 'scuess'
            return redirect(url_for('query_all'))
        except Exception as e:
            flash("{}".format(e))
            return 'failed'
    else:
        return render_template('student.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student = Student.query.filter_by(student_id=student_id).first()
        db.session.delete(student)
        db.session.commit()
        # return redirect(url_for('result'))
        return redirect(url_for('query_all'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        amount_due = request.form['amount_due']
        try:
            student = Student.query.get(student_id)
            student.first_name = first_name
            student.last_name = last_name
            student.dob = dob
            student.amount_due = amount_due
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('query_all'))
        except Exception as e:
            print(e)
            flash("{}".format(e))
            return redirect(url_for('/'))
    else:
        try:
            student_id = request.args.get('student_id')
            student = Student.query.get(student_id)
            return render_template('student_update.html', row=student)
        except Exception as e:
            print(e)
            flash("{}".format(e))
            return redirect(url_for('/'))


@app.route('/query_all')
def query_all():
    rows = None
    try:
        rows = Student.query.all()
        print('rows:', rows)
        return render_template('result.html', rows=rows, type=0)
    except Exception as e:
        flash("{}".format(e))
        print('error:', e)
    return 'failed'


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        s_id = request.form['student_id']
        rows = None
        rows = Student.query.filter_by(student_id=s_id)

        return render_template('result.html', rows=rows, type=1)
    else:
        return render_template('search.html')


if __name__ == '__main__':
    # db.drop_all() #first time run
    # db.create_all()#create table
    app.run(debug=False)
