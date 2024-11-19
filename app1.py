from flask import Flask, render_template, request, redirect, url_for, flash, session

# Initialize Flask application
app1 = Flask(__name__)
app1.secret_key = 'your_secret_key'  # Used for session management

# Hardcoded credentials for demonstration purposes (you can replace with a database later)
USER_CREDENTIALS = {
    'email': 'test@example.com',
    'password': 'password123'
}

@app1.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email and password match
        if email == USER_CREDENTIALS['email'] and password == USER_CREDENTIALS['password']:
            session['loggedin'] = True
            session['email'] = email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    
    return render_template('login.html')

@app1.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    return f'Welcome, {session["email"]}! You are logged in.'

@app1.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the Flask application in debug mode
if __name__ == "__main__":
    app1.run(debug=True, port=5001)
