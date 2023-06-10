from flask import Flask, request, jsonify
import psycopg2
import bcrypt

app = Flask(__name__)

db_config = {
    'database': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

def db_query(query, params=()):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    except psycopg2.DatabaseError as e:
        print(f"Error: {str(e)}")
        return None

@app.route('/signup', methods=['POST'])
def sign_up():
    # Register a new user
    data = request.get_json()
    # check if the email is already registered
    query = """SELECT id FROM Users WHERE email = %s;"""
    params = (data['email'],)
    result = db_query(query, params)
    if result is not None and len(result) > 0:
        # if email already exists, return an error
        return jsonify({"error": "Email already registered"}), 409  # 409 Conflict

    # if the email is not yet registered, proceed with user creation
    password = data['password'].encode('utf-8')  # Convert password to bytes
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())  # Generate a salt and hash the password

    query = """INSERT INTO Users (username, email, password) VALUES (%s, %s, %s) RETURNING id;"""
    params = (data['username'], data['email'], hashed)
    result = db_query(query, params)
    if result is not None:
        user_id = result[0][0]
        return jsonify({"user_id": user_id, "message": "User created"}), 201
    else:
        return jsonify({"error": "Error while creating user"}), 500

@app.route('/signin', methods=['POST'])
def sign_in():
    # Authenticate a user
    data = request.get_json()
    password = data['password'].encode('utf-8')  # Convert password to bytes

    query = """SELECT id, password FROM Users WHERE username = %s;"""
    params = (data['username'], )
    result = db_query(query, params)
    if result is not None and len(result) > 0:
        # Check the password against the hashed password stored in the database
        if bcrypt.checkpw(password, result[0][1].encode('utf-8')):
            return jsonify({"user_id": result[0][0], "message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/user_roles', methods=['GET'])
def get_user_roles():
    # Retrieve all user roles from the UserRoles table
    user_roles = db_query('SELECT * FROM UserRoles')
    if user_roles is not None:
        return jsonify(user_roles)
    else:
        return jsonify({"error": "Error while fetching user roles"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    # Validate user_id input
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id parameter is missing"}), 400
    if not user_id.isnumeric():
        return jsonify({"error": "user_id must be a number"}), 400

    # Retrieve user with the given user_id from the Users table
    query = "SELECT * FROM Users WHERE id = %s"
    user = db_query(query, (user_id, ))
    if user is not None and len(user) > 0:
        return jsonify(user[0]), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    # Add user to the Users table
    data = request.get_json()
    query = """INSERT INTO Users (username, email, phone, role_id, profile_image, community_page_url, profile_visibility, time_zone, display_name, title, personal_info, is_visible_to_all_members) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    params = (data['username'], data['email'], data['phone'], data['role_id'], data['profile_image'],
              data['community_page_url'], data['profile_visibility'], data['time_zone'],
              data['display_name'], data['title'], data['personal_info'],
              data['is_visible_to_all_members'])
    result = db_query(query, params)
    if result is not None:
        user_id = result[0][0]
        return jsonify({"user_id": user_id, "message": "User created"}), 201
    else:
        return jsonify({"error": "Error while creating user"}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Update user in the Users table
    data = request.get_json()
    query = """UPDATE Users SET username = %s, email = %s, phone = %s, role_id = %s, profile_image = %s, community_page_url = %s, profile_visibility = %s, time_zone = %s, display_name = %s, title = %s, personal_info = %s, is_visible_to_all_members = %s WHERE id = %s"""
    params = (data['username'], data['email'], data['phone'], data['role_id'], data['profile_image'],
              data['community_page_url'], data['profile_visibility'], data['time_zone'],
              data['display_name'], data['title'], data['personal_info'],
              data['is_visible_to_all_members'], user_id)
    result = db_query(query, params)
    if result is not None:
        return jsonify({"user_id": user_id, "message": "User updated"}), 200
    else:
        return jsonify({"error": "Error while updating user"}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Delete user from the Users table along with associated roles and followers
    query = """DELETE FROM UserRoles WHERE id = %s; DELETE FROM Followers WHERE user_id = %s OR follower_id = %s; DELETE FROM Users WHERE id = %s"""
    result = db_query(query, (user_id, user_id, user_id))
    if result is not None:
        return jsonify({"message": "User and associated roles and followers deleted"}), 200
    else:
        return jsonify({"error": "Error while deleting user"}), 500

@app.route('/followers/<int:id>', methods=['PUT'])
def update_follower(id):
    # Update a follower in the Followers table
    data = request.get_json()
    query = """UPDATE Followers SET user_id = %s, follower_id = %s WHERE id = %s"""
    params = (data['user_id'], data['follower_id'], id)
    result = db_query(query, params)
    if result is not None:
        return jsonify({"message": "Follower updated"}), 200
    else:
        return jsonify({"error": "Error while updating follower"}), 500

@app.route('/user_roles/<int:id>', methods=['PUT'])
def update_user_role(id):
    # Update a user role in the UserRoles table
    data = request.get_json()
    query = """UPDATE UserRoles SET role = %s WHERE id = %s"""
    params = (data['role'], id)
    result = db_query(query, params)
    if result is not None:
        return jsonify({"message": "User role updated"}), 200
    else:
        return jsonify({"error": "Error while updating user role"}), 500

if __name__ == '__main__':
    app.run(debug=True)
