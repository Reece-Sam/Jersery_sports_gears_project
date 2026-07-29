from flask import Blueprint, request, jsonify
from extensions import db
from models import Cart, CartItem, Product, User, Payment

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/<int:user_id>', methods = ['GET'])
def get_cart(user_id):
    """
    Gets a user's shopping cart
    ---
    tags:
      - Cart

    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user whose cart is being retrieved 

    responses: 
      200:
        description: Cart retrieved successfully (or empty cart)

      500:
        description: Internal server error     
    """

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
                "description" : item.product.description,
                "category" : item.product.category,
                "image-url" : item.product.image_url,
                "stock": item.product.stock,
                "size": item.size,
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
    """
    Add a product to the cart
    ---
    tags: 
      - Cart
    
    consumes:
      - application/json

    parameters:
      - in: body
        name: body
        required: true
        schema: 
          type: object
          required:
            - user_id 
            - product_id
          properties:
            user_id:
              type: integer
              example: 1
            product_id:
              type: integer
              example: 5
            quantity:
              type: integer
              example: 2

    responses: 
      200: 
        description: Item added to cart successfully

      400: 
        description: Missing fields or insufficient stock

      404: 
        description: User or product not found

      500: 
        description: Internal server error                 
    """

    try:

        data = request.get_json()

        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        size = data.get("size", "M")

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
            product_id=product_id,
            size=size
        ).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(
                cart_id = cart.id,
                product_id = product_id,
                quantity = quantity,
                size = size
            )
            db.session.add(new_item)

        db.session.commit()

        return jsonify({
            "status" : "success",
            "message" : "Item added to cart"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@cart_bp.route('/item/<int:item_id>', methods = ['DELETE'])
def remove_from_cart(item_id):
    """
    Remove an item from the cart
    ---
    tags: 
      - Cart
    
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: Cart item ID
    
    responses:
      200:
        description: Item removed successfully
      
      404: 
        description: Cart item not found
      
      500: 
        description: Internal server error
    """

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
            "status" : "success",
            "message" : "Item removed from cart"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@cart_bp.route('/item/<int:item_id>', methods = ['PATCH', 'PUT'])
def update_cart_item(item_id):
    """
    Update the quantity of a cart item
    ---
    tags:
      - Cart

    consumes:
      - application/json

    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: Cart item ID

      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - quantity
          properties:
            quantity:
              type: integer
              example: 3

    responses:
      200:
        description: Cart updated successfully

      400:
        description: Invalid quantity or insufficient stock

      404:
        description: Cart item not found

      500:
        description: Internal server error
    """

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
            "status" : "success",
            "message" : "Cart updated successfully"
        }), 200
    
    except Exception as e: 
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500


@cart_bp.route('/checkout/<int:user_id>', methods=['POST'])
def checkout(user_id):
    """
     Checkout a user's cart and create an order
    ---
    tags:
      - Cart

    consumes:
      - application/json

    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID

      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - payment_method
            - phone_number
          properties:
            payment_method:
              type: string
              enum:
                - mtn_mobile_money
                - orange_money
              example: mtn_mobile_money
            phone_number:
              type: string
              example: "677123456"

    responses:
      200:
        description: Checkout completed successfully

      400:
        description: Invalid payment method, empty cart, missing phone number, or insufficient stock

      404:
        description: User not found

      500:
        description: Internal server error
    """
    
    try:
        from models import Order, OrderItem, Payment

        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "status" : "error",
                "message" : "User not found"
            }), 404

        data = request.get_json()

        payment_method = data.get("payment_method")
        phone_number = data.get("phone_number")

        if not phone_number:
            return jsonify({
                "status" : "error",
                "message" : "Phone number is required"
            }), 400

        allowed_methods = [
            "mtn_mobile_money",
            "orange_money"
        ]

        if payment_method not in allowed_methods:
            return jsonify({
                "status": "error",
                "message": "Invalid payment method"
            }), 400

        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart or not cart.items:
            return jsonify({
                "status": "error",
                "message": "Cart is empty"
            }), 400

        total_price = 0

        order = Order(
            user_id=user_id,
            total_price=0,
            status="pending"
        )

        db.session.add(order)
        db.session.flush()

        for item in cart.items:

            product = item.product

            if product.stock < item.quantity:
                return jsonify({
                    "status": "error",
                    "message": f"Not enough stock for {product.name}"
                }), 400

            product.stock -= item.quantity

            subtotal = product.price * item.quantity
            total_price += subtotal

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            db.session.add(order_item)

        order.total_price = total_price 

        payment = Payment(
            order_id = order.id,
            payment_method = payment_method,
            phone_number = phone_number,
            amount = total_price,
            status = "pending"
        )

        db.session.add(payment)

        for item in cart.items:
            db.session.delete(item)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Checkout successful",
            "order_id": order.id,
            "payment_id" : payment.id,
           "payment_method": order.payment.payment_method,
           "payment_status": order.payment.status,
            "total_price": str(order.total_price)
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
