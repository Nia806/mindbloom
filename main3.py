from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "navynavya"

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///member.db"
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
        return redirect(url_for('dashboard3'))  # Redirect to dashboard if already logged in
    return render_template("index3.html")  # Changed template to index3.html



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the fields are empty
        if not username or not password:
            return render_template("index3.html", error="Username and password are required")
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('dashboard3'))
        else:
            return render_template("index3.html", error="Invalid username or password")
    return render_template("index3.html")



# Register route
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the fields are empty
    if not username or not password:
        return render_template("index3.html", error="Username and password are required")
    
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index3.html", error="Username already taken!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard3'))



# Dashboard route
@app.route("/dashboard3")
def dashboard3():
    if "username" in session:
        return render_template("dashboard3.html", username=session['username'])  # Changed template to dashboard3.html
    return redirect(url_for('home'))  # Redirect to home if not logged in


# Logout route
@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove 'username' from session
    return redirect(url_for('home'))  # Redirect to home after logout


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True, port=5050)
