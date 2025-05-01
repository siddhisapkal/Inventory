from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask app and database connection
app = Flask(__name__)
app.secret_key = 'kusumachandashwini'

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/studentdbms'  # Change to your database details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader function for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models

# User Model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(20), unique=True)
    sname = db.Column(db.String(100))
    sem = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    branch = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))

# Inventory Item Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Sales Model
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship('Item', backref=db.backref('sales', lazy=True))

# Routes for various pages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
@login_required
def inventory():
    items = Item.query.all()
    return render_template('inventory.html', items=items)

@app.route('/additem', methods=['POST', 'GET'])
@login_required
def add_item():
    if request.method == "POST":
        name = request.form.get('name')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        
        new_item = Item(name=name, category=category, quantity=int(quantity), price=float(price))
        db.session.add(new_item)
        db.session.commit()
        flash("Item Added Successfully", "success")
        return redirect(url_for('inventory'))

    return render_template('add_item.html')

@app.route('/edititem/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)  # Get the item by ID
    if request.method == "POST":
        # Update the item's attributes based on the form inputs
        item.name = request.form.get('name')
        item.category = request.form.get('category')
        item.quantity = request.form.get('quantity')
        item.price = request.form.get('price')
        db.session.commit()
        flash("Item Updated Successfully", "success")
        return redirect(url_for('inventory'))  # Redirect back to the inventory page

    return render_template('edit_item.html', item=item)  # Render the edit item template

@app.route('/deleteitem/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Item Deleted Successfully", "danger")
    return redirect(url_for('inventory'))


@app.route('/addstudent', methods=['POST', 'GET'])
@login_required
def add_student():
    if request.method == "POST":
        rollno = request.form.get('rollno')
        sname = request.form.get('sname')
        sem = request.form.get('sem')
        gender = request.form.get('gender')
        branch = request.form.get('branch')
        email = request.form.get('email')
        phone = request.form.get('num')
        address = request.form.get('address')
        
        # Create a new Student object
        new_student = Student(rollno=rollno, sname=sname, sem=sem, gender=gender, 
                              branch=branch, email=email, phone=phone, address=address)
        
        # Add the student to the database
        db.session.add(new_student)
        db.session.commit()
        
        flash("Student Added Successfully", "success")
        return redirect(url_for('add_student'))  # Redirect to the same page after adding

    # Department list to display on the form (this is passed to the template)
    dept = [
        {"branch": "Computer Science"},
        {"branch": "Electronics"},
        {"branch": "Mechanical"}
    ]
    
    return render_template('student.html', dept=dept)

@app.route('/editstudent/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        student.rollno = request.form.get('rollno')
        student.sname = request.form.get('sname')
        student.sem = request.form.get('sem')
        student.gender = request.form.get('gender')
        student.branch = request.form.get('branch')
        student.email = request.form.get('email')
        student.phone = request.form.get('num')
        student.address = request.form.get('address')
        db.session.commit()
        flash("Student Updated Successfully", "success")
        return redirect(url_for('index'))
    
    return render_template('edit_student.html', student=student)

@app.route('/deletestudent/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student Deleted Successfully", "danger")
    return redirect(url_for('index'))

@app.route('/sales')
@login_required
def sales():
    sales = Sale.query.all()
    return render_template('sales.html', sales=sales)

@app.route('/addsale', methods=['POST', 'GET'])
@login_required
def add_sale():
    if request.method == "POST":
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity')
        
        item = Item.query.get(item_id)
        if item and item.quantity >= int(quantity):
            item.quantity -= int(quantity)
            sale = Sale(item_id=item.id, quantity=int(quantity))
            db.session.add(sale)
            db.session.commit()
            flash("Sale Recorded Successfully", "success")
        else:
            flash("Insufficient Stock", "danger")
        return redirect(url_for('sales'))

    items = Item.query.all()
    return render_template('add_sale.html', items=items)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists.", "warning")
            return redirect(url_for('signup'))

        # Corrected password hashing method to 'pbkdf2:sha256'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful, please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successful", "warning")
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

if __name__ == "__main__":
    app.run(debug=True)
