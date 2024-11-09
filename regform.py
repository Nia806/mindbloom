# app.py
from flask import Flask, request, render_template
from flask_SQLAlchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Route to render the form
@app.route('/')
def index():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    # Create a new User record
    new_user = User(name=name, email=email, age=age)
    db.session.add(new_user)
    db.session.commit()

    return "Data submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)