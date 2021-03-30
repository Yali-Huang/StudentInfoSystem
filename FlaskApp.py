from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:////./data.db"  # local database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True


app = Flask(__name__)
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
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
            return redirect(url_for('query_all'))
        except Exception as e:
            flash("{}".format(e))
            return 'failed'


@app.route('/delete', methods=['POST', 'GET'])
def Delete():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student = Student.query.filter_by(student_id="唐家三少").first()
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('result'))


@app.route('/update', methods=['POST', 'GET'])
def Update():
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
            return redirect(url_for('result'))
        except Exception as e:
            flash("{}".format(e))
            return redirect(url_for('/'))


@app.route('/query_all')
def query_all():
    rows = None
    try:
        rows = Student.query.all()
        return render_template('result.html', rows=rows)
    except Exception as e:
        flash("{}".format(e))
    return 'failed'


@app.route('/search', methods=['POST', 'GET'])
def search():
    print('Search')
    if request.method == 'POST':
        student_id = request.form['student_id']
#         first_name  = request.form['first_name']
#         last_name  = request.form['last_name']
#         dob = request.form['dob']
#         amount_due = request.form['amount_due']

        rows = None

#         if( first_name ):
#            rows = Student.query.filter_by(first_name=first_name).all()

#         if( last_name ):
#            rows = Student.query.filter_by(last_name=last_name).all()

#         if( amount_due>0 ):
#            rows = Student.query.filter_by(amount_due>0).all()

        if(student_id):
            print(f'search {student_id}')
            rows = Student.query.filter_by(student_id=student_id).all()

        return render_template('result.html', rows=rows)

    return 'Failed'


if __name__ == '__main__':
    # db.drop_all() #the first time run this
    # db.create_all()#create table
    app.run(debug=False)
