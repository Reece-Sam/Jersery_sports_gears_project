from flask import Blueprint, request, jsonify
from extensions import db
from models import Product 

product_bp = Blueprint('product_bp', __name__)


@product_bp.route('/products', methods=['POST'])
def create_product():
   
    data = request.get_json()

    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')

    if not name or price is None or stock is None:
        return jsonify({
            "status": "error",
            "message": "Missing required fields"
        }), 400

    product = Product(
        name=name,
        description=data.get('description'),
        price=price,
        stock=stock,
        category=data.get('category'),
        image_url=data.get('image_url')
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Product created successfully"
    }), 201


@product_bp.route('/products', methods=['GET'])
def get_products():
     """
    Get All Products
    ---
    tags:
      - Product
    responses:
      200:
        description: List of products
    """
     
     products = products.query.all()

     result = []
     for product in products:
         result.append ({
             "id": product.id,
             "name": product.name,
             "price": product.price,
             "stock": product.stock,
             "category": product.category,
             "image_url": product.image_url
         })
    
     return jsonify(result), 200 


@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):

    product = db.session.get(Product, id)

    if product is None:
        return jsonify({
            "status" : "error",
            "message" : "Product not found"
        }), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category": product.category,
        "image_url": product.image_url
    }), 200

