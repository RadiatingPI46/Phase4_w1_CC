from flask import jsonify, request, Blueprint
from models import db, User
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)

# =================================================================================================================================================================================
# adding a user
@user_bp.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    print("Email ",check_email)
    print("Username",check_username)

    if check_username and check_email:
        return jsonify({"error":"Username and email exists"})
    
    elif check_username:
        return jsonify({"error":"Username exists"})
    
    elif check_email:
        return jsonify({"error":"Email exists"})
    
    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success":"Added successfully"})
    
# ===============================================================================================================================================================================

# Update a user
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_users(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get('username', user.username)
        email = data.get('email', user.email)
        password = data.get('password', user.password)

        check_username = User.query.filter_by(username=username and id!=user.id).first()
        check_email = User.query.filter_by(email=email and id!=user.id).first()

        if check_username and check_email:
            return jsonify({"error":"Username and email exists"})
        
        elif check_username:
            return jsonify({"error":"Username exists"})
        
        elif check_email:
            return jsonify({"error":"Email exists"})
        
        else:
            user.username=username
            user.email=email
            user.password=password
          
            db.session.commit()
            return jsonify({"success":"Updated successfully"})

    else:
        return jsonify({"error":"User doesn't exist!"})

# =================================================================================================================================================================================
# Delete
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_users(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success":"Deleted successfully"}), 200

    else:
        return jsonify({"error":"User your are trying to delete doesn't exist!"})
# =================================================================================================================================================================================
# Get all users
@user_bp.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            "collection":[
                {
                    "id": collection.id,
                    "name_of_item": collection.name_of_item,
                    "item_type": collection.item_type,
                    "price_of_item": collection.price_of_item,
                    "item_description": collection.item_description 
                } for collection in user.collection
            ]}
        output.append(user_data)
        return jsonify({"users":output})

# =================================================================================================================================================================================