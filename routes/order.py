from flask import Blueprint, request, jsonify
from extensions import db
from models import Order, OrderItem, Product, User

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods = ['POST'])
def create_order():

    try: 
        data = request.get_json()

        user_id = data.get('user_id')
        items = data.get('item')

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
                db.seesion.add(order_item)

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
    

@order_bp.route('/orders', methods = ['GET'])
def get_orders():
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
    

@order_bp.route('orders/<int:id>', methods = ['GET'])
def get_order(id):
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
    


