from flask import Blueprint, request, jsonify
from extensions import db
from models import Order, OrderItem, Product, User
from services.order_service import create_order_from_cart


def create_order_from_cart(user_id):
    try:
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        cart_items = user.cart_items  

        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 400

        total = 0

        order = Order(
            user_id=user.id,
            status="pending",
            total_price=0
        )

        db.session.add(order)
        db.session.flush()  # get order.id before commit

        for item in cart_items:
            product = db.session.get(Product, item.product_id)

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            total += product.price * item.quantity
            db.session.add(order_item)

        order.total_price = total

        for item in cart_items:
            db.session.delete(item)

        db.session.commit()

        return jsonify({
            "status": "success",
            "order_id": order.id,
            "total": str(total)
        }), 201

    except Exception as e:
        return jsonify({
            "status" : "error", 
            "message" : str(e)
        }), 500