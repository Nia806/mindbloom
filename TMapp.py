from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    


@app.route('/show')
def products():
    allTask = Task.query.all()
    print(allTask)
    return 'This is the products page'



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/work')
def work():
    return render_template('work.html')



@app.route('/scholarship')
def scholarship():
    return render_template('scholarship.html')



@app.route('/mentorship')
def mentorship():
    return render_template('mentorship.html')



@app.route('/session')
def session():
    return render_template('session.html')



@app.route('/impact')
def impact():
    return render_template('impact.html')



@app.route('/newsletter')
def newsletter():
    return render_template('newsletter.html')



@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')



@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Task.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")
        
    task = Task.query.filter_by(sno=sno).first()
    return render_template('update.html', task=task)

 
@app.route('/delete/<int:sno>')
def delete(sno):
    task = Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def hello_world(): 
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Task(title=title, desc=desc)
        db.session.add(task)
        db.session.commit()

    allTask = Task.query.all()
    print(allTask)
    return render_template('index.html', allTask=allTask)


if __name__ == "__main__":
    # Create all the tables in the database
    with app.app_context():  
        db.create_all()  # This will create the task.db database if it doesn't exist
    
    # Run the application in debug mode
    app.run(debug=True, port=5002)