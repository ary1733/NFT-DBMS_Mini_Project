from flask import Blueprint, make_response, request, jsonify, session
from APP.utils import query_db, query_commit_db, api_session_required


user_bp = Blueprint('user', __name__)

@user_bp.route("/get")
def get_users():
    query_res = query_db('select * from user')
    response = make_response(
                jsonify(
                    {"message": query_res}
                ),
                200,
            )
    # return query_db('select * from user')
    return response

@user_bp.route("/get_info")
@api_session_required # this checks for session
def get_all_info():
    data = session.get('user')
    if(data.get('email') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    
    userData = {"Email_Id": data.get("email")}
    
    # Fetch mobile Numbers
    query_res = query_db('select DISTINCT Mobile_Number from User_Mobile_Number WHERE Email_Id = ?', (data.get('email'), ))
    userData["Mobile_Number"] = query_res

    # Fetch Addresses
    query_res = query_db('select DISTINCT * from Address WHERE Email_Id = ?', (data.get('email'), ))
    userData["Address"] = query_res

    # Fetch Name
    query_res = query_db('select Name from User WHERE Email_Id = ?', (data.get('email'), ), one=True)
    userData["Name"] = query_res["Name"]

    response = make_response(
                jsonify(
                    {"message": userData}
                ),
                200,
            )
    # return query_db('select * from user')
    return response

@user_bp.route("/add/", methods = ["POST"])
def add_users():
    data = request.json
    print(data)
    # return data
    query_res = True
    if(data.get('Email_Id') is None or data.get('Name') is None or data.get('Password') is None):
        return make_response(jsonify({"message": "failure"}), 200)
    if(data.get('Name') is not None):
        query_res = query_commit_db(
            """
            INSERT INTO User (Email_Id, Name) values
            (?, ?)
            """,
            (data['Email_Id'], data['Name']),
            one=True
        )

    if(data.get('Mobile_Number') is not None):
        query_res = query_commit_db(
            """
            INSERT INTO User_Mobile_Number (Mobile_Number, Email_id) values (?, ?);
            """,
            [(number, data['Email_Id'],) for number in data['Mobile_Number']]
        )

    if(data.get('Address') is not None):
        query_res = query_commit_db(
            """
            INSERT INTO Address (House_No, Street, City, Country, PinCode, Email_Id) values (?, ?, ?, ?, ?, ?);
            """,
            [(House_No, Street, City, Country, PinCode, data['Email_Id'],) for House_No, Street, City, Country, PinCode in data['Address']]
        )
    
    if(data.get('Password') is not None):
        query_res = query_commit_db(
            """
            INSERT INTO LoginDetails (Email_ID, Password) values
            (?, ?)
            """,
            [(data['Email_Id'], data['Password'],)]
        )
    

    return make_response(jsonify({"message": "success" if query_res else "failure"}), 200)


@user_bp.route("/login/" , methods = ["POST"])
def login():
    session.pop("user", None)
    data = request.json
    if(data.get('email') is None):
        return make_response(jsonify({"message": "Email not sent"}), 200)
    
    if(data.get('password') is None):
        return make_response(jsonify({"message": "Password not sent"}), 200)
    
    query_res = query_db('select Email_Id from LoginDetails WHERE Email_Id = ? and Password = ?', (data.get('email'), data.get('password')), True)
    response = make_response(
                jsonify(
                    {"message": "failure"}
                ),
                200,
            )
    print(query_res)
    if(query_res is not None ):
        session['user'] = {
            'email': query_res['Email_Id']
        }
        response = make_response(
                jsonify(
                    {
                        "message": "success",
                        "email":query_res['Email_Id']
                    }
                ),
                200,
            )
    return response

@user_bp.route("/getwishlist")
@api_session_required
def getwishlist():
    data = session.get('user')
    query_res = query_db('''
    SELECT Item.* FROM Wishlist
    JOIN User on Wishlist.Email_Id = User.Email_Id
    JOIN Item on Wishlist.Item_Id = Item.Item_Id
    WHERE User.Email_Id = ?'''
    , (data.get('email'),),
    )
    return jsonify(query_res)

# Harshit
def like_item():
    data = request.json
    if(data.get('Email_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Email Id"}), 200)
    if(data.get('Item_Id') is None):
        return make_response(jsonify({"message": "Not a Valid Item Id"}), 200)
    query_res = query_commit_db(
        """
        INSERT into Wishlist (Email_Id, Item_Id) values (?, ?)
        """,
        (data.get('Email_Id'), data.get('Item_Id')),
        True
    )
    return make_response(jsonify({"message": query_res}), 200)