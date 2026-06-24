from flask import Blueprint, request, jsonify
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_mail import Message
from extensions import db, mail
from models import User


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users

    consumes:
      - application/json

    parameters:
      - in: body
        name: body
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
              example: "677123456"
            password:
              type: string
              example: password123

    responses:
      201:
        description: User created successfully

      400:
        description: Missing fields or email already exists

      500:
        description: Internal server error
    """

    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Invalid or missing JSON body"
            }), 400

        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not name or not email or not phone_number or not password:
            return jsonify({
                "status": "fail",
                "message": "Missing required field"
            }), 400

        # Check if us
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({
                "status": "error",
                "message": "Email already exists"
            }), 400

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        # Send welcome email
        msg = Message(
            subject="Welcome to Sports Store",
            sender="bebsyanski@gmail.com",
            recipients=[email]
        )

        msg.body = f"""
Hello {name},

Welcome to Sports Store!

Your account has been created successfully.

Thank you for joining us.
"""

        mail.send(msg)

        return jsonify({
            "status": "success",
            "message": "User created successfully",
            "user_id": user.id
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@user_bp.route('/login', methods=['POST'])
def login_user():
    """
    Login user
    ---
    tags:
      - Users

    consumes:
      - application/json

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: john@gmail.com
            password:
              type: string
              example: password123

    responses:
      200:
        description: Login successful

      400:
        description: Email and password required

      401:
        description: Invalid credentials

      500:
        description: Internal server error
    """

    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({
                "status" : "error",
                "message": "Email and password are required"
            }), 400

        user = User.query.filter_by(
            email=email,
            is_deleted=False
        ).first()
 

        if not user or not check_password_hash(user.password, password):
            return jsonify({
                "status" : "error",
                "message": "Invalid credentials"
            }), 401

        return jsonify({
            "status" : "success",
            "message": "Login successful",
            "user_id": user.id
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

@user_bp.route('/', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users

    responses:
      200:
        description: List of users

      500:
        description: Internal server error
    """
   
    try:
        users = User.query.filter_by(is_deleted=False).all()

        return jsonify([{
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        } for user in users]), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    """
    Get a user by ID
    ---
    tags:
      - Users

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: User ID

    responses:
      200:
        description: User found

      404:
        description: User not found

      500:
        description: Internal server error
    """
   
    try:
        user = User.query.filter_by(
            id=id,
            is_deleted=False
        ).first()

        if user is None:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
        
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@user_bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update_user(id):
    """
    Update user details
    ---
    tags:
      - Users

    consumes:
      - application/json

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: User ID

      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: John Smith
            phone_number:
              type: string
              example: "675987654"
            password:
              type: string
              example: newpassword123

    responses:
      200:
        description: User updated successfully

      404:
        description: User not found

      500:
        description: Internal server error
    """
   
    try: 
        user = db.session.get(User, id)

        if not user:
          return jsonify({
              "status" : "error",
              "message" : "User not found"
          }), 404

        data = request.get_json()

        if 'name' in data:
          user.name = data['name']

        if 'phone_number' in data:
          user.phone_number = data['phone_number']

        if 'password' in data:
          user.password = generate_password_hash(data['password'])

        db.session.commit()

        return jsonify({
            "status" : "success",
            "message": "User updated successfully",
              "user": {
              "id": user.id,
              "name": user.name,
              "phone_number": user.phone_number
            }
    }), 200

    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500


@user_bp.route('/<int:id>', methods = ['DELETE'])
def delete_user(id):
    """
    Soft delete a user
    ---
    tags:
      - Users

    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: User ID

    responses:
      200:
        description: User deleted successfully

      400:
        description: User already deleted

      404:
        description: User not found

      500:
        description: Internal server error
    """

    try:
        user = db.session.get(User, id)

        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
        
        if user.is_deleted:
            return jsonify({
                "status": "error",
                "message": "User already deleted"
            }), 400

        user.is_deleted = True
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "User deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500






# def delete_user(id):

#     try:
#         user = db.session.get(User, id)

#         if not user:
#             return jsonify({
#                 "status": "error",
#                 "message": "User not found"
#             }), 404

#         print("USER:", user.id)
#         print("ORDERS:", user.orders)

#         db.session.delete(user)
#         db.session.commit()

#         return jsonify({
#             "status": "success",
#             "message": "User deleted successfully"
#         }), 200

#     except Exception as e:
#         db.session.rollback()

#         print("ERROR:", e)

#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500




# def delete_user(id):
    
#     try:
#         user = db.session.get(User, id)

#         if not user:
#             return jsonify({
#                 "status" : "error",
#                 "message" : "User not found"
#             }), 404
        
#         db.session.delete(user)
#         db.session.commit()

#         return jsonify({
#            "status" : "success",
#            "message" : "User deleted successfully"
#         }), 200
    
#     except Exception as e:
#         return jsonify({
#             "status" : "error",
#             "message" : str(e)
#         }), 500
    