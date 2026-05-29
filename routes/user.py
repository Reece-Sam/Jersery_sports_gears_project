from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash 


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():

    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not name or not email or not phone_number or not password:
            return jsonify({
                "status" : "fail",
                "message" : "Missing required field"
            }), 400

        # check if user exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({
                "status" : "error",
                "message": "Email already exists"
            }), 400

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
            "status" : "Success",
            "message": "User created successfully",
            "user_id": user.id
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@user_bp.route('/users/login', methods=['POST'])
def login_user():

    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({
                "status" : "error",
                "message": "Email and password are required"
            }), 400

        user = User.query.filter_by(email=email).first()

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
    

@user_bp.route('/users', methods=['GET'])
def get_users():
   
    try:
        users = User.query.all()

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


@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
   
    try:
        user = db.session.get(User, id)

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


@user_bp.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    
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


@user_bp.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    
    try:
        user = db.session.get(User, id)

        if not user:
            return jsonify({
                "status" : "error",
                "message" : "User not found"
            }), 404
        
        db.session.delete(user)
        db.session.commit()

        return jsonify({
           "status" : "success",
           "message" : "User deleted successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500
    