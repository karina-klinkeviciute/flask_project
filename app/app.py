import os

from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from pymongo import MongoClient

from models import db, Product, User, Post, UserProfile, Tag
from dotenv import load_dotenv


load_dotenv()

client = MongoClient("mongodb://mongo:27017/")
mongo_db = client.mydatabase
collection = mongo_db.mycollection

app: Flask = Flask(__name__)


# database initiation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new2.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db.init_app(app)
migrate = Migrate(app, db)

# admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserProfile, db.session))
admin.add_view(ModelView(Product, db.session))

class TagView(ModelView):
    column_hide_backrefs = False
    column_list = ("name", "posts")

admin.add_view(TagView(Tag, db.session))

class PostView(ModelView):
    column_list = ("title", "content", "author")
    column_hide_backrefs = False

admin.add_view(PostView(Post, db.session))


# class UserView(ModelView):
#     column_hide_backrefs = False
#     column_list = ('email', 'active', 'roles')

# login
login_manager = LoginManager(app)
login_manager.login_view = 'home'


@app.route('/mongo_index/')
def index():
    # Insert a document into MongoDB
    collection.insert_one({"message": "Hello from MongoDB!"})

    # Retrieve documents from MongoDB
    documents = collection.find()

    message = ""
    for doc in documents:
        message += doc["message"] + "<br>"

    return f"<h1>{message}</h1>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bcrypt = Bcrypt(app)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


# routes
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


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
