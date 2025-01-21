from flask import jsonify, request, Blueprint
from models import db, User, TokenBlocklist
from werkzeug.security import check_password_hash
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app import app, mail
from flask_mail import Message

auth_bp= Blueprint("auth_bp", __name__)

# ==================================================================================================================================================================================================
# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password ) :
        access_token = create_access_token(identity=user.id)
        print(access_token)
        try:
            msg = Message(
                subject="Welcome to the Collections App",
                sender=app.config["MAIL_DEFAULT_SENDER"],
                recipients=[email],
                body=f"Your token is {access_token}"

            )
            mail.send(msg)
            return jsonify({"access_token": access_token}), 200
        except Exception as e:
            return "Failed to send email"
    


    else:
        return jsonify({"error": "Either email/password is incorrect"})
    
# ==================================================================================================================================================================================================

# current user
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    current_user_id  = get_jwt_identity()

    user =  User.query.get(current_user_id)
    user_data = {
            'id':user.id,
            'email':user.email,
            'username':user.username
        }

    return jsonify(user_data)

# ==================================================================================================================================================================================================

# Logout
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"success ":"Logged out successfully"})

# ==================================================================================================================================================================================================