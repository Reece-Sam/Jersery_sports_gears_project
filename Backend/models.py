from datetime import datetime
from sqlalchemy import func
from extensions import db


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    orders = db.relationship(
        'Order',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User: {self.email}>'
    

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(
        db.DateTime,
        server_default = func.now(),
        nullable = False 
    )

    name = db.Column(db.String(150), nullable = False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2), nullable = False)
    stock = db.Column(db.Integer, default = 0)
    
    category = db.Column(db.String(100), nullable = False)
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<Product: {self.name}>'
    
    
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default="pending")
    


    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship(
         'User',
         back_populates='orders'
    )

    items = db.relationship(
        'OrderItem',
        back_populates='order',
        cascade='all, delete-orphan'
    )

    payment = db.relationship(
        'Payment',
        back_populates='order',
        uselist=False,
        cascade='all, delete-orphan'
    )


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id'),
        nullable=False,
        unique=True
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False
    )

    phone_number = db.Column(
        db.String(20),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )

    transaction_id = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False
    )

    order = db.relationship(
        'Order',
        back_populates='payment'
    )



class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id'),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship(
        'Order',
        back_populates='items'
    )

    product = db.relationship('Product')


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False
    )

    user = db.relationship('User', backref='cart')


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)

    cart = db.relationship("Cart", backref="items")
    product = db.relationship('Product')

    