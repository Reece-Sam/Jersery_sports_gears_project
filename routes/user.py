from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash 


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
Create User (Register)
---
tags:
  - Users
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      required:
        - name
        - email
        - phone_number
        - password
      properties:
        name:
          type: string
          example: John Doe
        email:
          type: string
          example: john@gmail.com
        phone_number:
          type: string
          example: "237612345678"
        password:
          type: string
          example: password123
responses:
  201:
    description: User created successfully
  400:
    description: Missing fields or user exists
"""

    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not name or not email or not phone_number or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)

    user = User(
        name=name,
        email=email,
        phone_number=phone_number,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user_id": user.id
    }), 201



@user_bp.route('/users/login', methods=['POST'])
def login_user():
    """
Login User
---
tags:
  - Users
"""

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id
    }), 200