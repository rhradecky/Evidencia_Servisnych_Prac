from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://upkjsca8ynbl11b0ikgz:f1nKXzsR6eivAWjmQDT6i6W0E7b2vG@bdipmw29ejuoeccxynb1-postgresql.services.clever-cloud.com:50013/bdipmw29ejuoeccxynb1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

users = {
    'john': 'password123',
    'jane': 'mypassword'
}

class Evidencia(db.Model):
    __tablename__ = 'evidencia'
    radio_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_number = db.Column(db.String(10), nullable=False)
    fw = db.Column(db.String(4), nullable=False)
    uroven = db.Column(db.String(2), nullable=False)
    faktura = db.Column(db.String(8), nullable=False)
    datum = db.Column(db.Date, nullable=False)














@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('welcome', username=username))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')



@app.route('/welcome/<username>')
def welcome(username):
    records = Evidencia.query.all()
    return render_template('home.html', username=username, records=records)

if __name__ == '__main__':
    app.run(debug=True)