from flask import Flask
from flasgger import Swagger
from extensions import db, mail
from dotenv import load_dotenv
from flask_cors import CORS
from models import User, Product, Cart, CartItem, Order, OrderItem
from routes.user import user_bp
from routes.product import product_bp
from routes.cart import cart_bp
from routes.order import order_bp
from flask_mail import Mail


import os

load_dotenv()
app = Flask(__name__)

CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')

db.init_app(app)
mail.init_app(app)

# Swagger docs
Swagger(app)

#Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

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
    return "Sports Store API Running "


if __name__ == "__main__":
    app.run(debug=True)
   
