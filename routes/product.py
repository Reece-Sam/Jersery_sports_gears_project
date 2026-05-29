from flask import Blueprint, request, jsonify
from extensions import db
from models import Product 

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():

    try:
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

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@product_bp.route('/products', methods=['GET'])
def get_products():

    try:
        products = Product.query.all()

        result = []

        for product in products:
            result.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "category": product.category,
                "image_url": product.image_url
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):

    try:
        product = db.session.get(Product, id)

        if product is None:
            return jsonify({
                "status": "error",
                "message": "Product not found"
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

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@product_bp.route('/products/<int:id>', methods=['PATCH', 'PUT'])
def update_product(id):
   
    try:
        product = db.session.get(Product, id)

        if product is None:
            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400

        if 'name' in data:
            product.name = data['name']

        if 'description' in data:
            product.description = data['description']

        if 'price' in data:
            product.price = data['price']

        if 'stock' in data:
            product.stock = data['stock']

        if 'category' in data:
            product.category = data['category']

        if 'image_url' in data:
            product.image_url = data['image_url']

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Product Updated Successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@product_bp.route('/products/<int:id>', methods = ['DELETE'])
def delete_product(id):

    try:
        product = db.session.get(Product, id)

        if product is None:
            return jsonify({
                "status" : "error",
                "message" : "Product not found"
            }), 404
        
        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "status" : "success",
            "message" : "Product deleted successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500


