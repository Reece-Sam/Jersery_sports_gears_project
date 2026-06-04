from flask import Blueprint, request, jsonify
from extensions import db
from models import Cart, CartItem, Product, User

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/<int:user_id>', methods = ['GET'])
def get_cart(user_id):

    try:
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            return jsonify({
                "status":"error",
                "message":"Cart is empty", "items":[], "total": 0
            }), 200
        
        items = []
        total = 0

        for item in cart.items:
            subtotal = item.product.price * item.quantity
            total += subtotal

        
            items.append({
                "cart_item_id" : item.id,
                "product_id" : item.product.id,
                "product_name" : item.product.name,
                "quantity" : item.quantity,
                "price" : str(item.product.price),
                "subtotal" : str(subtotal)
            })  
        
        return jsonify({
            "cart_id" : cart.id,
            "items" : items,
            "total" : str(total)
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@cart_bp.route('/add', methods = ['POST'])
def add_to_cart():
    try:

        data = request.get_json()

        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        if not user_id or not product_id:
            return jsonify({
                "status" : "error",
                "message" : "Missing required feilds"
            }), 400
        
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({
                "status" : "error",
                "message" : "User not found"
            }), 404
        
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({
                "status" : "error", 
                "message" : "Product not found"
            }), 404
        
        if product.stock < quantity:
            return jsonify({
                "status" : "error",
                "message" : "Not enough stock"
            }), 400
        
        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.flush()
        
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(
                cart_id = cart.id,
                product_id = product_id,
                quantity = quantity
            )
            db.session.add(new_item)

        db.session.commit()

        return jsonify({
            "status" : "error",
            "message" : "Item added to cart"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@cart_bp.route('/carts/item/<int:item_id>', methods = ['DELETE'])
def remove_from_cart(item_id):
    try:
        item = db.session.get(CartItem, item_id)

        if not item:
            return jsonify({
                "status" : "error",
                "message" : "Item not found"
            }), 404
        
        db.session.delete(item)
        db.session.commit()

        return jsonify({
            "status" : "error",
            "message" : "Item removed from cart"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@cart_bp.route('carts/item/<int:item_id>', methods = ['PATCH', 'POST'])
def update_cart_item(item_id):
    try:
        item = db.session.get(CartItem, item_id)

        if not item:
            return jsonify({
                "status" : "error",
                "message" : "Item not found"
            }), 404 
        
        data = request.get_json()
        quantity = data.get('quantity')

        if quantity is None or quantity < 1 :
            return jsonify({
                "status" : "error",
                "message" : "Invalid quantity"
            }), 400
        
        if item.product.stock < quantity:
            return jsonify({
                "status" : "error", 
                "message" : "Not enough stock"
            }), 400
        
        item.quantity = quantity
        db.session.commit()

        return jsonify({
            "status" : "error",
            "message" : "Cart updated successfully"
        }), 200
    
    except Exception as e: 
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500


@cart_bp.route('carts/checkout/<int:user_id>', methods = ['POST'])
def checkout(user_id):
    try: 

        from models import Order, OrderItem 

        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart or not cart.items:
            return jsonify({
                "status":"error", 
                "message":"Cart is empty"
            }), 400
        
        total_price = 0

        order = Order(
            user_id = user_id,
            total_price = 0,
            status = "pending"
        )

        db.session.add(order)
        db.session.flush()

        for item in cart.items:
            product = item.product

            if product.stock < item.quantity:
                return jsonify({
                    "status" : "error",
                    "message" : f"Not enough stock for {product.name}"
                }), 400
            
            product.stock -= item.quantity

            subtotal = product.price * item.quantity
            total_price += subtotal

            order_item = OrderItem(
                order_id = order.id,
                product_id = product.id, 
                quantity = item.quantity, 
                price = product.price
            )
            
            db.session.add(order_item)
        
        order.total_price = total_price

        for item in cart.items:
            db.session.delete(item)

        db.session.commit()

        return jsonify({
            "status" : "success",
            "message" : "Checkout successful",
            "order_id" : order.id,
            "total_price" : str(order.total_price)
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500

