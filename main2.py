from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "navynavya"

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mentor.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard2'))  # Redirect to dashboard if already logged in
    return render_template("index2.html")  # Render the updated index2.html


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Check for empty fields
        if not username or not password:
            return render_template("index2.html", error="Username and password are required")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('dashboard2'))
        else:
            return render_template("index2.html", error="Invalid username or password")
    return render_template("index2.html")


# Register route
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check for empty fields
    if not username or not password:
        return render_template("index2.html", error="Username and password are required")

    # Check if the username is already taken
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index2.html", error="Username already taken!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard2'))



# Dashboard route
@app.route("/dashboard2")
def dashboard2():
    if "username" in session:
        return render_template("dashboard2.html", username=session['username'])  # Render the updated dashboard2.html
    return redirect(url_for('home'))  # Redirect to home if not logged in


# Logout route
@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove 'username' from session
    return redirect(url_for('home'))  # Redirect to home after logout


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True, port=7000)
