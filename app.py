from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from models import db, Product, User


app: Flask = Flask(__name__)

# database initiation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

# admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))

# login
login_manager = LoginManager(app)
login_manager.login_view = 'home'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bcrypt = Bcrypt(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


# routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', message='user with this email already exists')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
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
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid email or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/contacts/")
def contacts():
    user_display_name = current_user.display_name
    return render_template("contacts.html", contacts='my phone number is 555 123456', user_display_name=user_display_name)


@app.route("/products/")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)


@app.route("/products/<int:product_id>/")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product.html", product=product)


@app.route("/example/<name>")
def example(name):
    return render_template("example_template.html", name=name)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)
    app.run(debug=True)
