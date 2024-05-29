from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from models import db, Product, User

from products import all_products

app: Flask = Flask(__name__)

# database initiation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

# admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))

# routes
@app.route('/')
def home():
    return render_template('index.html', email=session.get("email"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', message='user with this email already exists')
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['email'] = email
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid email or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route("/contacts/")
def contacts():
    return render_template("contacts.html", contacts='my phone number is 555 123456', email=session.get("email"))


@app.route("/products/")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products, email=session.get("email"))


@app.route("/products/<int:product_id>/")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product.html", product=product, email=session.get("email"))


@app.route("/example/<name>")
def example(name):
    return render_template("example_template.html", name=name, email=session.get("email"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)
    app.run(debug=True)
