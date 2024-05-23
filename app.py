from flask import Flask, Response, render_template

from products import all_products

app: Flask = Flask(__name__)


@app.route("/")
def hello():
    return 'Hello World!'


@app.route("/contacts/")
def contacts():
    return 'my phone number is 555 123456'


@app.route("/products/")
def products():
    products = all_products
    return render_template("products.html", products=products)


@app.route("/products/<int:product_id>/<name>")
def product(product_id, name):
    return f'{all_products[product_id][0]} sold to {name}, price: {all_products[product_id][1]}'

@app.route("/example/<name>")
def example(name):
    return render_template("example_template.html", name=name)



if __name__ == "__main__":
    app.run(debug=True)
