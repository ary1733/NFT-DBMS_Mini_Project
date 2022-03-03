# Item Base Structure

from flask import Blueprint, make_response, request, jsonify
from APP.utils import query_db, query_commit_db

item_bp = Blueprint('item', __name__)

# View 
@item_bp.route("/get",methods=["POST"])
def get_item():
    data = request.json
    print(data)
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    
    # Get Items using Email Id
    query_res = query_db('select * from Item WHERE Email_Id = ?', (data.get('Email_Id'), ))
    
    response = make_response(
                jsonify(
                    {"message": query_res}
                ),
                200,
            )
    return response

# Create
@item_bp.route("/add/", methods=["POST"])
def add_item():
    data = request.json
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    
    query_res = False
    # Atleast Expect a name field
    if(data.get('Name') is not None):
        query_res = query_commit_db(
            """
            INSERT INTO Item (Name, Description, Email_Id) values
            (?, ?, ?)
            """,
            (data.get('Name'), data.get('Description'), data.get('Email_Id')),
            True
        )
    return make_response(jsonify({"message": query_res}), 200)

# Delete
@item_bp.route("/delete/", methods=["POST"])
def delete_item():
    data = request.json
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)

    query_res = query_commit_db(
        """
        DELETE FROM Item WHERE Item_Id = ? AND Email_Id = ?;
        """,
        (data.get('Item_Id'), data.get('Email_Id')),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)

# Update
@item_bp.route("/update/", methods=["POST"])
def update_item():
    data = request.json
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)

    query_res = query_commit_db(
        """
        UPDATE Item
        SET
        Name = ?,
        Description = ?
        WHERE
        Item_ID = ?
        AND
        Email_ID = ?
        """,
        (data.get('Name'), data.get('Description'),data.get('Item_Id'), data.get('Email_Id')),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)
    

