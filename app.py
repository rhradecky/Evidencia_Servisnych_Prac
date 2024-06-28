from flask import Flask, render_template, session, request, redirect, url_for, flash, send_file, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pandas as pd
import os
from io import StringIO


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'blablabla'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://upkjsca8ynbl11b0ikgz:f1nKXzsR6eivAWjmQDT6i6W0E7b2vG@bdipmw29ejuoeccxynb1-postgresql.services.clever-cloud.com:50013/bdipmw29ejuoeccxynb1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class Evidencia(db.Model):
    __tablename__ = 'evidencia'
    radio_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_number = db.Column(db.String(10), nullable=False)
    fw = db.Column(db.String(4), nullable=False)
    uroven = db.Column(db.String(2), nullable=False)
    faktura = db.Column(db.String(8), nullable=False)
    datum = db.Column(db.Date, nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('welcome', username=username))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Boli ste úspešne odhlásený')
    return redirect(url_for('login'))


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('welcome', username=session['username']))
    return redirect(url_for('login'))


@app.route('/welcome/<username>')
def welcome(username):
    records = Evidencia.query.all()
    return render_template('home.html', username=username, records=records)


@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        serial_number = request.form['serial_number']
        fw = request.form['fw']
        uroven = request.form['uroven']
        faktura = request.form['faktura']
        datum = request.form['datum']

        new_record = Evidencia(serial_number=serial_number, fw=fw, uroven=uroven, faktura=faktura, datum=datum)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('welcome', username=session['username']))
    return render_template('add_device.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        serial_number = request.form.get('serial_number')
        fw = request.form.get('fw')
        uroven = request.form.get('uroven')
        faktura = request.form.get('faktura')
        datum = request.form.get('datum')

        query = Evidencia.query
        if serial_number:
            query = query.filter_by(serial_number=serial_number)
        if fw:
            query = query.filter_by(fw=fw)
        if uroven:
            query = query.filter_by(uroven=uroven)
        if faktura:
            query = query.filter_by(faktura=faktura)
        if datum:
            query = query.filter_by(datum=datum)

        results = query.all()

    return render_template('search.html', results=results)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        import_csv_to_db(file_path)
        return redirect(url_for('welcome', username=session['username']))


@app.route('/export')
def export_data():
    records = Evidencia.query.all()
    data = []

    for record in records:
        data.append({
            'serial_number': record.serial_number,
            'fw': record.fw,
            'uroven': record.uroven,
            'faktura': record.faktura,
            'datum': record.datum
        })

    df = pd.DataFrame(data)
    csv_output = StringIO()
    df.to_csv(csv_output, index=False)
    csv_output.seek(0)

    response = make_response(csv_output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=export.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


def import_csv_to_db(file_path):
    data = pd.read_csv(file_path)
    for i, row in data.iterrows():
        new_record = Evidencia(
            serial_number=row['serial_number'],
            fw=row['fw'],
            uroven=row['uroven'],
            faktura=row['faktura'],
            datum=row['datum']
        )
        db.session.add(new_record)
    db.session.commit()
    os.remove(file_path)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
