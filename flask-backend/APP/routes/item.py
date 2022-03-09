import datetime

# Item Base Structure
from flask import Blueprint, make_response, request, jsonify, session
from APP.utils import query_db, query_commit_db, api_session_required

item_bp = Blueprint('item', __name__)

#TODO: Make Advert Id as Primary Key with Autoincrement
#TODO: Make Bid Id as Primary Key with Autoincrement
#TODO: Add API routes for search_item, bid, add_advert

# View 
@item_bp.route("/get",methods=["GET"])
@api_session_required
def get_item():
    data = session.get('user')
    print(data)
    if(data.get('email') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    
    # Get Items using Email Id
    query_res = query_db('select * from Item WHERE Email_Id = ?', (data.get('email'), ))
    
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

#* Bhushan
def search_item():
    data = request.json
    searchTerm = data.get('SearchTerm')
    # ! CHECKS
    if(searchTerm is None):
        return make_response(jsonify({"message": "Not a Valid Search Term"}), 200)
    
    query_res = query_db(
        """
        GET Item 
        WHERE Name LIKE ?
        """,
        (searchTerm),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)

def bid():
    data = request.json
     # ! CHECKS
    if(data.get('Advert_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Advert Id"}), 200)
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Cost') is None):
        return make_response(jsonify({"message": "Not a Valid Cost"}), 200)
    
    query_res = query_commit_db(
        """
        INSERT INTO Bid (Advert_Id, Email_Id, Cost) values
        (?, ?, ?)
        """,
        (data.get('Advert_Id'), data.get('Email_Id'), data.get('Cost')),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)
        
def add_advert():
    data = request.json
    # ! CHECKS
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)
    if(data.get('Cost') is None):
        return make_response(jsonify({"message": "Not a Valid Cost"}), 200)

    query_res = query_commit_db(
        """
        INSERT INTO SaleAdvertisement (Email_Id,Item_Id, Date) values
        (?, ?, ?);
        SELECT Advert_Id as AID FROM SaleAdvertisement WHERE Email_Id = ? AND Item_Id = ?;
        INSERT INTO Bid (Advert_Id, Email_Id, Cost) values
        (AID, ?, ?);
        """,
        (data.get('Email_Id'), data.get('Item_Id'), datetime.datetime.now(), data.get('Email_Id'), data.get('Item_Id'), data.get('Email_Id'), data.get('Cost')),
        True
    )

    return make_response(jsonify({"message": query_res}), 200)

# Harshit
def write_review():
    data = request.json
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)
    if(data.get('Review') is None):
        return make_response(jsonify({"message": "Not a Valid Review"}), 200)
    if(data.get('Rating') is None):
        return make_response(jsonify({"message": "Not a Valid Rating"}), 200)
    query_res = query_commit_db(
        """
        INSERT INTO Review (Email_Id, Item_Id, Review, Rating) values
        (?, ?, ?, ?)
        """,
        (data.get('Email_Id'), data.get('Item_Id'), data.get('Review'), data.get('Rating')),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)

def sell_item():
    data = request.json
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Advertisement_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Advertisement Id"}), 200)
    query_res = query_commit_db(
        """
        UPDATE SaleAdvertisement
        SET End_Date = ?
        WHERE
        Advert_Id = ?;
        SELECT Cost as cost, Email_Id as eid FROM Bid WHERE Advert_Id = ?
        ORDER BY Cost DESC LIMIT 1;
        SELECT Item_Id as iid FROM SaleAdvertisement WHERE Advert_Id = ?;
        UPDATE Item
        SET
        Email_Id = eid
        WHERE
        Item_Id = iid;
        INSERT INTO Transactons (Cost, Date, Item_Id, BuyerEmail_Id, SellerEmail_Id) values
        (cost, ?, iid, eid, ?);
        """,
        (datetime.datetime.now(), data.get('Advertisement_Id'), data.get('Advertisement_Id'), data.get('Advertisement_Id'), datetime.datetime.now(), data.get('Email_Id'), data.get('Email_Id')),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)

def get_history():
    data = request.json
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)
    query_res = query_db(
        """
        with t as (
            SELECT * FROM Transactons
            WHERE Item_Id = ?
        )
        with recursive rec_history(seller, buyer) as (
            select SellerEmail_Id, BuyerEmail_Id
            from t
            union
            select rec_history.seller, t.BuyerEmail_Id
            from rec_history, t
            where rec_history.buyer = t.SellerEmail_Id
        )
        SELECT * FROM rec_history
        """,
        (data.get('Item_Id'), )
    )
    return make_response(jsonify({"message": query_res}), 200)