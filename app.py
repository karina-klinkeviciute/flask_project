from flask import Flask, Response, render_template

from products import all_products

app: Flask = Flask(__name__)


@app.route("/")
def hello():
    return 'Hello World!'


@app.route("/contacts/")
def contacts():
    return render_template("contacts.html", contacts='my phone number is 555 123456')


@app.route("/products/")
def products():
    products = all_products
    return render_template("products.html", products=products)


@app.route("/products/<int:product_id>/")
def product(product_id):
    product = all_products[product_id]
    return render_template("product.html", product=product)


@app.route("/example/<name>")
def example(name):
    return render_template("example_template.html", name=name)



if __name__ == "__main__":
    app.run(debug=True)
