import datetime

# Item Base Structure
from flask import Blueprint, make_response, request, jsonify, session
from APP.utils import query_db, query_commit_db, api_session_required

item_bp = Blueprint('item', __name__)

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
@api_session_required
def add_item():
    data = dict(request.form)
    data['Email_Id'] = session.get('user').get('email')
    imageFiles = request.files.getlist("Image")
    
    # return make_response(jsonify({"message":"ok"}))
    query_res = True
    # Atleast Expect a name field
    if(data.get('Name') is not None):
        query_res &= query_commit_db(
            """
            INSERT INTO Item (Name, Description, Email_Id) values
            (?, ?, ?)
            """,
            (data.get('Name'), data.get('Description'), data.get('Email_Id')),
            True
        )
    ItemId = query_db(
        """
        select seq from sqlite_sequence where name=?;
        """,
        ("Item",),
        True).get('seq')    
    if(request.files['Image'].filename != ''):
        prepareList = []
        for file in imageFiles:
            imgData = file.read()
            prepareList.append((imgData, ItemId))
        query_res &= query_commit_db('''
        INSERT INTO Item_Image (Image, Item_Id) values
        (?, ?)
        ''',
        prepareList
        )
    else:
        print("No files")
    return make_response(jsonify({"message": "success" if query_res else "failure"}), 200)


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
        (searchTerm, ),
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

@item_bp.route('/add_advert', methods=["POST"])        
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
        INSERT INTO SaleAdvertisement (Item_Id, Date) values
        (?, ?);
        """,
        (data.get('Item_Id'), datetime.datetime.now()),
        True)
    AID = query_db(
        """
        select seq from sqlite_sequence where name=?;
        """,
        ("SaleAdvertisement",),
        True)
    query_res &= query_commit_db(
        """
        INSERT INTO Bid (AdvertisementId, Bidder_Id, Cost, Date) values
        (?, ?, ?, ?);
        """,
        (AID.get("seq"), data.get('Email_Id'), data.get('Cost'), datetime.datetime.now(),),
        True
    )

    return make_response(jsonify({"message": query_res}), 200)

# Harshit
@item_bp.route("/write_review", methods=["POST"])
# @api_session_required
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
        INSERT INTO Reviews (Email_Id, Item_Id, Review, Rating, Date) values
        (?, ?, ?, ?, ?)
        """,
        (data.get('Email_Id'), data.get('Item_Id'), data.get('Review'), data.get('Rating'), datetime.datetime.now()),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)
# Fetch can't request get with body, hence we need to use post
@item_bp.route("/get_review", methods=["POST"])
# @api_session_required
def get_review():
    data = request.json
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)
    query_res = query_db(
        """
        SELECT * FROM Reviews WHERE Item_Id = ?;
        """,
        (data.get('Item_Id'),)
    )
    return make_response(jsonify({"message": query_res}), 200)

@item_bp.route("/sell/", methods=["POST"])
def sell_item():
    data = request.json
    email_id = data.get('Email_Id')
    advert_id = data.get('AdvertisementId')

    # ! CHECKS
    if(email_id is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(advert_id is None):
        return make_response(jsonify({"message": "Not a Valid Advertisement Id"}), 200)
    
    
    # ! if Advertisement Exists
    advert = query_db(
        """
        SELECT count(*) as cnt FROM SaleAdvertisement 
        WHERE AdvertisementId = ?
        and
        End_Date is NULL;
        """,
        (advert_id,),
    )
    advert = advert[0]
    if(advert.get("cnt") == 0):
        return make_response(jsonify({"message": "Advertisement does not exist"}), 200)
    
    # ! Should be checked while creating the advertisement
    if(advert.get("cnt") > 1):
        return make_response(jsonify({"message": "Advertisement is not unique"}), 200)

    query_res = query_commit_db(
        """
        UPDATE SaleAdvertisement
        SET End_Date = ?
        WHERE
        AdvertisementId = ?
    """,
        (datetime.datetime.now(), advert_id),
        True
    )

    highest_bid = query_db(
        """
        SELECT Cost as cost, Bidder_Id as eid FROM Bid WHERE AdvertisementId = ?
        ORDER BY Cost DESC LIMIT 1
        """,
        (advert_id,),
    )

    highest_bid = highest_bid[0]

    item = query_db(
        """
        SELECT Item_Id as iid FROM SaleAdvertisement WHERE AdvertisementId = ?
        """,
        (advert_id,),
    )

    item = item[0]

    query_res &= query_commit_db(
        """
        UPDATE Item
        SET
        Email_Id = ?
        WHERE
        Item_Id = ?
        """,
        (highest_bid.get('eid'), item.get('iid')),
        True
    )

    query_res &= query_commit_db(
        """
        INSERT INTO Transactions (Cost, Date, Item_Id, BuyerEmail_Id, SellerEmail_Id) values
        (?, ?, ?, ?, ?);
        """,
        (highest_bid.get('cost'), datetime.datetime.now(), item.get('iid'), email_id, highest_bid.get('eid'),),
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