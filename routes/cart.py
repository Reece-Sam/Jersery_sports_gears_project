from flask import Blueprint, request, jsonify
from extensions import db
from models import Cart, CartItem, Product, User

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/cart/<int:user_id>', methods = ['GET'])
def get_cart(user_id):

    try:
        cart = Cart.query.filter_by(user_id=user_id).first()