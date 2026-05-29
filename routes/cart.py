from flask import Blueprint, request, jsonify
from extensions import db
from models import Cart, CartItem, Product, User

cart_bp = Blueprint('cart_bp', __name__)

