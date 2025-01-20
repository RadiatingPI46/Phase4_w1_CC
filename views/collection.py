from flask import jsonify, request, Blueprint
from models import db, Collection
from flask_jwt_extended import jwt_required, get_jwt_identity

collection_bp= Blueprint("collection_bp", __name__)

# ========================================================================================================================================================================
# Add collection
@collection_bp.route("/collection/add", methods=["POST"])
@jwt_required()
def add_collection():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    name_of_collection = data['name_of_collection']
    item_type = data['item_type']
    item_price = data['item_price']
    item_description = data['item_description']

    new_collection = Collection(name_of_collection=name_of_collection, item_type=item_type, item_price=item_price, item_description=item_description,user_id=current_user_id,)
    db.session.add(new_collection)
    db.session.commit()
    return jsonify({"success":"Collection added successfully"})

# ========================================================================================================================================================================

# UPDATE
@collection_bp.route("/collection/<int:collection_id>", methods=["PUT"])
@jwt_required()
def update_collection(collection_id):
    current_user_id = get_jwt_identity()

    data = request.get_json()
    collection = Collection.query.get(collection_id)

    if collection and collection.user_id==current_user_id:

        name_of_collection = data.get('name_of_collection', collection.name_of_collection)
        item_type = data.get('item_type', collection.item_type)
        item_price=data.get('item_price', collection.item_price)
        item_description = data.get('item_description',collection.item_description)

        # Apply updates
        collection.name_of_collection = name_of_collection
        collection.item_type = item_type
        collection.item_price = item_price
        collection.item_description = item_description

        db.session.commit()
        return jsonify({"success": "Collection updated successfully"})

    else:
        return jsonify({"error": "Collection not found/Unauthorized"})
    
# ========================================================================================================================================================================

# DELETE
@collection_bp.route("/collection/<int:collection_id>", methods=["DELETE"])
@jwt_required()
def delete_collection(collection_id):
    current_user_id = get_jwt_identity()

    collection = Collection.query.filter_by(id=collection_id, user_id=current_user_id).first()

    if not collection:
        return jsonify({"error": "Collection not found/Unauthorized"})


    db.session.delete(collection)
    db.session.commit()
    return jsonify({"success": "Collection deleted successfully"})

# ========================================================================================================================================================================
# Get all collections
@collection_bp.route("/Collections", methods=["GET"])
@jwt_required()
def get_collections():
    current_user_id = get_jwt_identity()

    collections = Collection.query.filter_by(user_id = current_user_id)

    collection_list = [
        {
            "id": collection.id,
            "name_of_item": collection.name_of_item,
            "item_type": collection.item_type,
            "item_price": collection.item_price,
            "item_description": collection.item_description,
            "user_id": collection.user_id,
            "user": {"id":collection.user.id, "username": collection.user.username, "email": collection.user.email},
        } for collection in collections
    ]    

    return jsonify(collection_list)

# ========================================================================================================================================================================

#  Get collection by ID
@collection_bp.route("/collection/<int:collection_id>", methods=["GET"])
@jwt_required()
def get_collection(collection_id):
    current_user_id = get_jwt_identity()

    collection = Collection.query.filter_by(id=collection_id, user_id=current_user_id).first()
    if collection:
        collection_details = {
            "id": collection.id,
            "name_of_item": collection.name_of_item,
            "item_type": collection.item_type,
            "item_price": collection.item_price,
            "item_description": collection.item_description,
            "user_id": collection.user_id
        }
        return jsonify(collection_details)
    
    else:
        return jsonify({"error": "Collection not found"})