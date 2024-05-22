from flask import Flask, Response

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
    products = """
    <html><head><title>Products</title></head>
    <body>
    <ul>
        <li>Product 1</li>
        <li>Product 2</li>
        <li>Product 3</li>
    </ul>
    </body>
    </html>
    """
    return products


@app.route("/products/<int:product_id>/<name>")
def product(product_id, name):
    return f'{all_products[product_id][0]} sold to {name}, price: {all_products[product_id][1]}'



if __name__ == "__main__":
    app.run(debug=True)
