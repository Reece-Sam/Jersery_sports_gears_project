from flask import Blueprint, request, jsonify
from extensions import db
from models import Order, OrderItem, Product, User
from services.order_service import create_order_from_cart

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods = ['POST'])
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders

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
            - items
          properties:
            user_id:
              type: integer
              example: 1
            items:
              type: array
              items:
                type: object
                required:
                  - product_id
                  - quantity
                properties:
                  product_id:
                    type: integer
                    example: 2
                  quantity:
                    type: integer
                    example: 3

    responses:
      201:
        description: Order created successfully

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
        items = data.get('items')

        if not user_id or not items:
            return jsonify({
                "status" : "error",
                "message" : "Missing required fields"
            }), 400
        
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({
                "status" : "error",
                "message" : "User not found"
            }), 404
        
        total_price = 0
        order_items = []

        for item in items:

            product = db.session.get(Product, item['product_id'])

            if not product:
                return jsonify({
                    "status":"error",
                    "message": f"Product {item['product_id']} not found"
                }), 404
            
            if product.stock < item['quantity']:
                return jsonify({
                    "status" : "error",
                    "message" : f"Not enough stock for {product.name}"
                }), 400
            
            price = product.price * item['quantity']
            total_price += price

            order_items.append({
                "product" : product, 
                "quantity" : item['quantity'],
                "price" : product.price
            })

            product.stock -= item['quantity']

        order = Order(
            user_id = user_id,
            total_price = total_price,
            status = "pending"
        )

        db.session.add(order)
        db.session.flush()

        for item in order_items:
            order_item = OrderItem(
                order_id = order.id,
                product_id = item["product"].id,
                quantity = item["quantity"],
                price = item["price"]
            )
            db.session.add(order_item)

        db.session.commit()

        return jsonify({
            "status" : "Success",
            "message" : "Order created successfully",
            "order_id" : order.id,
            "total_price" : str(order.total_price),
            "status" : order.status
        }), 201
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@order_bp.route('/from-cart/<int:user_id>', methods=['POST'])
def create_order_from_cart(user_id):
    """
    Create an order from the user's cart
    ---
    tags:
      - Orders

    parameters:
      - name: user_id
        in: path
        required: true
        type: integer

    responses:
      201:
        description: Order created successfully

      400:
        description: Cart is empty

      404:
        description: User not found

      500:
        description: Internal server error
    """
    return create_order_from_cart(user_id)
    

@order_bp.route('/', methods = ['GET'])
def get_orders():
    """
    Get all orders
    ---
    tags:
      - Orders

    responses:
      200:
        description: List of all orders

      500:
        description: Internal server error
    """

    try:

        orders = Order.query.all()

        result = []
        for order in orders:
            result.append({
                "id": order.id,
                "user_id": order.user_id,
                "total_price": str(order.total_price),
                "status": order.status,
                "created_at": order.created_at
        })

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    

@order_bp.route('/<int:id>', methods = ['GET'])
def get_order(id):
    """
    Get an order by ID
    ---
    tags:
      - Orders

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: Order ID

    responses:
      200:
        description: Order retrieved successfully

      404:
        description: Order not found

      500:
        description: Internal server error
    """
  
    try:
        order = db.session.get(Order, id)

        if not order:
            return jsonify({
                "status" : "error", 
                "message" : "Order not found"
            }), 404
        
        items = []
        for item in order.items:
            items.append({
                "product": item.product.name,
                "quantity": item.quantity,
                "price": str(item.price)
          })
            
        return jsonify({
            "status" : "success",
            "id": order.id,
            "user": order.user.name,
            "total_price": str(order.total_price),
            "status": order.status,
            "items": items
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error", 
            "message" : str(e)
        }), 500
    

@order_bp.route('/<int:id>/cancel', methods = ['PATCH'])
def cancel_order(id):
    """
    Cancel an order
    ---
    tags:
      - Orders

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: Order ID

    responses:
      200:
        description: Order cancelled successfully

      400:
        description: Order is already cancelled

      404:
        description: Order not found

      500:
        description: Internal server error
    """

    try:
        order = db.session.get(Order, id)

        if not order:
            return jsonify({
               "status" : "error",
               "message" : "Order not found"
            }), 404
    
        if order.status == "cancelled":
            return jsonify({
              "status" : "error",
              "message" : "Already Cancelled"
            }), 400
    
        for item in order.items:
            item.product.stock += item.quantity

        order.status = "cancelled"

        db.session.commit()

        return jsonify({
            "status" : "success",
            "message" : "Order Cancelled Successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500


@order_bp.route('/<int:id>/status', methods=['PUT'])
def update_order_status(id):
    """
    Update an order's status
    ---
    tags:
      - Orders

    consumes:
      - application/json

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: Order ID

      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum:
                - pending
                - paid
                - shipped
                - delivered
                - cancelled
              example: shipped

    responses:
      200:
        description: Order status updated successfully

      400:
        description: Invalid order status

      404:
        description: Order not found

      500:
        description: Internal server error
    """

    try:
        order = db.session.get(Order, id)

        if not order:
            return jsonify({"message": "Order not found"}), 404

        data = request.get_json()
        new_status = data.get("status")

        allowed = ["pending", "paid", "shipped", "delivered", "cancelled"]

        if new_status not in allowed:
            return jsonify({
                "message": "Invalid status"
            }), 400

        order.status = new_status
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Order status updated",
            "order_id": order.id,
            "new_status": order.status
        }), 200

    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500


@order_bp.route('/<int:id>', methods = ['DELETE'])
def delete_order(id):
    """
    Delete an order
    ---
    tags:
      - Orders

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: Order ID

    responses:
      200:
        description: Order deleted successfully

      404:
        description: Order not found

      500:
        description: Internal server error
    """

    try: 
        order = db.session.get(Order, id)

        if not order:
            return jsonify({
                "status" : "error",
                "message" : "Order not found"
            }), 404
        
        db.session.delete(order)
        db.session.commit()

        return jsonify({
            "status" : "success",
            "message" : "Order deleted successfully"
        }), 200
    
    except Exception as e: 
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
