from flask import Flask
from flasgger import Swagger
from extensions import db
from dotenv import load_dotenv
from flask_cors import CORS

# Import new models
from models import User, Product, Cart, CartItem, Order, OrderItem

# Import new routes
from routes.user import user_bp
from routes.product import product_bp
from routes.cart import cart_bp
from routes.order import order_bp

import os

load_dotenv()
app = Flask(__name__)

# Enable CORS
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Optional but important for auth later
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')

db.init_app(app)

# Swagger docs
Swagger(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(cart_bp, url_prefix="/api/cart")
app.register_blueprint(order_bp, url_prefix="/api/orders")


# Create tables
with app.app_context():
    # db.drop_all()  # careful with this in production
    db.create_all()


@app.route('/')
def home():
    return "Sports Store API Running 🚀"


if __name__ == "__main__":
    app.run(debug=True)
