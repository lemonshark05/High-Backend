import json
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, url_for, request, jsonify, render_template, send_file, session, flash, send_from_directory
from data import db, Comment, User, Blog, UserRole, Message, UserExperience, University, UserImage, UserVideo, Scholarship, handle_error, Crud, Follower
import os
import pdfkit
from sqlalchemy import or_
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user
from uuid import uuid4

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # (**deploy should delete this line)Solve the problem about http to https
app = Flask(__name__, static_folder='static', template_folder='.')
app.config.from_object('config.Config')
app.secret_key = "mysecretkey"  # Replace with your secret key

# Configure the Google OAuth2.0
google_blueprint = make_google_blueprint(
    client_id=app.config.get("GOOGLE_OAUTH_CLIENT_ID"),  # Get Client ID from Config
    client_secret=app.config.get("GOOGLE_OAUTH_CLIENT_SECRET"),  # Get Client Secret from Config
    scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
)
app.register_blueprint(google_blueprint, url_prefix="/google_login")
# initialize
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/uploads'
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/home")
def home_page():
    return render_template('front/home.html')

@app.route("/")
def home():
    return render_template('front/home.html')

@app.route("/login")
def login_html():
    return render_template('front/login-1.html')

@app.route("/login_email")
def login_email_html():
    return render_template('front/login-2.html')

@app.route("/register")
def register_html():
    return render_template('front/register.html')

@app.route("/more-info")
def more_info_html():
    return render_template('front/more-info.html')

@app.route("/connect")
def connect_html():
    return render_template('front/connect.html')

@app.route("/explore")
def explore_html():
    return render_template('front/explore.html')

@app.route("/resources")
def resources_html():
    return render_template('front/resources.html')

@app.route("/scholarship")
def scholarship_html():
    return render_template('front/scholarship.html')

@app.route("/university")
def university_html():
    return render_template('front/university.html')

@app.route("/search")
def search_html():
    return render_template('front/search.html')

@app.route("/signup")
def signup_html():
    return render_template('front/signup.html')

# Google mail login API
@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        email = resp.json()["email"]

        # Check if user exists in your database
        user = User.query.filter_by(email=email).first()

        # If user exists, log them in
        if user:
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))

        # If user does not exist, redirect to sign up page with user email
        else:
            session['email'] = email
            return redirect(url_for('register'))

    except TokenExpiredError:
        return redirect(url_for("google.login"))

@app.route("/logininfo", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    records = Crud.read(User, filters={'username': username})
    if not records:
        return jsonify({'error': 'user not found'}), 404

    records = Crud.read(User, filters={'username': username})
    if not records:
        return jsonify({'error': 'user not found'}), 404

    user = records[0]
    password_hash = user.get_password()
    if password_hash is None:
        return jsonify({'error': 'User has no password'}), 404
    if not check_password_hash(password_hash, password):
        return jsonify({'error': 'wrong password'}), 401

    return jsonify({'message': 'login successfully'}), 200

@app.route("/register/account", methods=["POST"])
def register():
    data = request.get_json()
    pwd = generate_password_hash(data['password'])  # hash the password
    repwd = generate_password_hash(data['repassword'])  # hash the repassword
    if pwd != repwd:
        return jsonify({'error': 'password not matched'}), 400
    user = User(username=data['username'], email=data['email'], password=pwd)
    try:
        Crud.create(user)
    except IntegrityError:
        db.session.rollback()  # necessary to continue using the session
        return jsonify({'error': 'username or email already in use'}), 400
    return redirect(url_for('register_interest'))

@app.route("/register/interest")
def register_interest():
    data = request.get_json()
    users = Crud.read(User, filters={"username": data['username']})
    if not users:
        return jsonify({'error': 'User not found'}), 404
    user = users[0]
    coaches = data['coaches']
    coach_json = json.dumps(coaches)
    Crud.update(user, interested_in_coaches=coach_json)
    return redirect(url_for('register/moreinfo'))

@app.route("/register/moreinfo")
def register_moreinfo():
    data = request.get_json()
    users = Crud.read(User, filters={"username": data['username']})
    if not users:
        return jsonify({'error': 'User not found'}), 404
    user = users[0]
    Crud.update(user, display_name=data['display_name'], title=data['title'], about_me=data['about_me'])
    return jsonify({'message':'Register successfully!'}), 204

# User
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Get the user
    users = Crud.read(User, filters={"id": user_id})

    if not users:  # If the list is empty, the user was not found
        return jsonify({'error': 'User not found'}), 404

    # Since id is unique, the list should contain only one user
    user = users[0]
    user_dict = user.to_dict()

    # Get user's role
    role = Crud.read(UserRole, filters={"id": user.role_id})

    # Get user's images
    user_images = Crud.read(UserImage, filters={"user_id": user_id})

    # Get user's videos
    user_videos = Crud.read(UserVideo, filters={"user_id": user_id})

    # Get user's experiences
    user_experiences = Crud.read(UserExperience, filters={"user_id": user_id})

    # Add related data to the user_dict
    user_dict["role"] = role[0].to_dict() if role else None
    user_dict["images"] = [image.to_dict() for image in user_images]
    user_dict["videos"] = [video.to_dict() for video in user_videos]
    user_dict["experiences"] = [experience.to_dict() for experience in user_experiences]

    # Return the user_dict which includes user data and related data
    return jsonify(user_dict)

# Blog
@app.route('/blogs', methods=['POST'])
def create_blog():
    data = request.get_json()
    blog = Blog(**data)
    Crud.create(blog)
    return jsonify(blog.to_dict()), 201

@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blogs = Crud.read(Blog, filters={"id": blog_id})

    if not blogs:  # If the list is empty, the blog was not found
        return jsonify({'error': 'Blog not found'}), 404

    # Since id is unique, the list should contain only one blog
    blog = blogs[0]
    blog_dict = blog.to_dict()

    # Getting comments for this blog
    comments = Crud.read(Comment, filters={"blog_id": blog_id})

    # Serializing comments to dict and add it to the blog_dict
    blog_dict["comments"] = [comment.to_dict() for comment in comments]

    # Return the blog_dict which includes blog data and its comments
    return jsonify(blog_dict)

@app.route('/blogs/all', methods=['GET'])
def get_all_blogs():
    blogs = Crud.read(Blog, order_by=['-id'])
    return jsonify([blog.to_dict() for blog in blogs])

@app.route('/blogs', methods=['GET'])
def get_blogs():
    # Get the page number (default None if not supplied)
    page = request.args.get('page', type=int, default=None)

    # Get the number of results per page (default None if not supplied)
    per_page = request.args.get('per_page', type=int, default=None)

    # Get filters if any
    filters = {}
    type = request.args.get('type')  # Get the type from query parameters
    if type:
        filters['type'] = type

    # Get search query
    search = request.args.get('search')

    query = Blog.query

    if filters:
        for key, value in filters.items():
            query = query.filter(getattr(Blog, key) == value)

    if search:
        search = f"%{search}%"  # Add percentage sign for matching any string
        query = query.filter(or_(Blog.title.ilike(search), Blog.content.ilike(search)))

    if page and per_page:
        pagination = query.order_by(Blog.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        # Convert the blogs to dictionaries
        blogs_dict = [blog.to_dict() for blog in pagination.items]
    else:
        blogs = query.order_by(Blog.id.desc()).all()
        blogs_dict = [blog.to_dict() for blog in blogs]

    return jsonify(blogs_dict)

@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.get_json()
    blogs = Crud.read(Blog, filters={"id": blog_id})
    if blogs is None:
        return jsonify({'error': 'Blog not found'}), 404
    # Since id is unique, the list should contain only one blog
    blog = blogs[0]
    Crud.update(blog, **data)
    return jsonify(blog.to_dict())

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blogs = Crud.read(Blog, filters={"id": blog_id})
    if blogs is None:
        return jsonify({'error': 'Blog not found'}), 404
    # Since id is unique, the list should contain only one blog
    blog = blogs[0]
    Crud.delete(blog)
    # Delete Comments about the Blog
    return jsonify({'message': 'Blog deleted successfully'}), 204

# University

@app.route('/universities', methods=['POST'])
def create_university():
    data = request.get_json()
    university = University(**data)
    Crud.create(university)
    return jsonify(university.to_dict()), 201

@app.route('/universities/<int:university_id>', methods=['GET'])
def get_university(university_id):
    universities = Crud.read(University, filters={"id": university_id})
    if not universities:
        return jsonify({'error': 'University not found'}), 404
    university = universities[0]
    return jsonify(university.to_dict())

@app.route('/universities/all', methods=['GET'])
def get_all_universities():
    universities = Crud.read(University)
    return jsonify([university.to_dict() for university in universities])

@app.route('/universities', methods=['GET'])
def get_universities():
    # Get the page number (default None if not supplied)
    page = request.args.get('page', type=int, default=None)
    per_page = request.args.get('per_page', type=int, default=None)

    # Get search query
    search = request.args.get('search')

    query = University.query

    if search:
        search = f"%{search}%"  # Add percentage sign for matching any string
        query = query.filter(University.name.ilike(search))

    if page and per_page:
        pagination = query.order_by(University.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        # Convert the universities to dictionaries
        universities_dict = [university.to_dict() for university in pagination.items]
    else:
        universities = query.order_by(University.id.desc()).all()
        universities_dict = [university.to_dict() for university in universities]

    return jsonify(universities_dict)

@app.route('/universities/<int:university_id>', methods=['PUT'])
def update_university(university_id):
    data = request.get_json()
    universities = Crud.read(University, filters={"id": university_id})
    if not universities:
        return jsonify({'error': 'University not found'}), 404
    university = universities[0]
    Crud.update(university, **data)
    return jsonify(university.to_dict())

@app.route('/universities/<int:university_id>', methods=['DELETE'])
def delete_university(university_id):
    universities = Crud.read(University, filters={"id": university_id})
    if not universities:
        return jsonify({'error': 'University not found'}), 404
    university = universities[0]
    Crud.delete(university)
    return jsonify({'message': 'University deleted successfully'}), 204

# Scholarship
@app.route('/scholarships', methods=['POST'])
def create_scholarship():
    data = request.get_json()
    scholarship = Scholarship(**data)
    Crud.create(scholarship)
    return jsonify(scholarship.to_dict()), 201

@app.route('/scholarships/<int:scholarship_id>', methods=['GET'])
def get_scholarship(scholarship_id):
    scholarships = Crud.read(Scholarship, filters={"id": scholarship_id})

    if not scholarships:  # If the list is empty, the scholarship was not found
        return jsonify({'error': 'Scholarship not found'}), 404

    # Since id is unique, the list should contain only one scholarship
    scholarship = scholarships[0]
    scholarship_dict = scholarship.to_dict()
    return jsonify(scholarship_dict)

@app.route('/scholarships/all', methods=['GET'])
def get_all_scholarships():
    scholarships = Crud.read(Scholarship)
    scholarship_list = [scholarship.to_dict() for scholarship in scholarships]
    return jsonify(scholarship_list)

@app.route('/scholarships', methods=['GET'])
def get_scholarships():
    # Get the page number (default None if not supplied)
    page = request.args.get('page', type=int, default=None)
    per_page = request.args.get('per_page', type=int, default=None)

    # Get filters if any
    filters = {}
    type = request.args.get('type')  # Get the type from query parameters
    university_id = request.args.get('university_id', type=int)  # Get the university_id from query parameters
    country = request.args.get('country')  # Get the country from query parameters
    if type:
        filters['type'] = type
    if university_id:
        filters['university_id'] = university_id
    if country:
        filters['country'] = country

    # Get search query
    search = request.args.get('search')

    query = Scholarship.query

    if filters:
        for key, value in filters.items():
            query = query.filter(getattr(Scholarship, key) == value)

    if search:
        search = f"%{search}%"  # Add percentage sign for matching any string
        query = query.filter(or_(Scholarship.type.ilike(search), Scholarship.description.ilike(search)))

    if page and per_page:
        pagination = query.order_by(Scholarship.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        # Convert the scholarships to dictionaries
        scholarships_dict = [scholarship.to_dict() for scholarship in pagination.items]
    else:
        scholarships = query.order_by(Scholarship.id.desc()).all()
        scholarships_dict = [scholarship.to_dict() for scholarship in scholarships]

    return jsonify(scholarships_dict)

@app.route('/scholarships/<int:scholarship_id>', methods=['PUT'])
def update_scholarship(scholarship_id):
    data = request.get_json()
    scholarships = Crud.read(Scholarship, filters={"id": scholarship_id})

    if not scholarships:  # If the list is empty, the scholarship was not found
        return jsonify({'error': 'Scholarship not found'}), 404

    # Since id is unique, the list should contain only one scholarship
    scholarship = scholarships[0]
    Crud.update(scholarship, **data)
    return jsonify(scholarship.to_dict())

@app.route('/scholarships/<int:scholarship_id>', methods=['DELETE'])
def delete_scholarship(scholarship_id):
    scholarships = Crud.read(Scholarship, filters={"id": scholarship_id})

    if not scholarships:  # If the list is empty, the scholarship was not found
        return jsonify({'error': 'Scholarship not found'}), 404

    # Since id is unique, the list should contain only one scholarship
    scholarship = scholarships[0]
    Crud.delete(scholarship)
    return jsonify({'message': 'Scholarship deleted'})

#Follower and Follow
@app.route('/followers', methods=['POST'])
def create_follower_relationship():
    data = request.get_json()
    follower = Follower(**data)
    Crud.create(follower, check_foreign_keys={"User": follower.user_id, "User": follower.follower_id})
    return jsonify(follower.to_dict()), 201

@app.route('/followers/<int:id>', methods=['GET'])
def get_follower_relationship(id):
    followers = Crud.read(Follower, filters={"id": id})
    if not followers:
        return jsonify({'error': 'Follower relationship not found'}), 404
    follower = followers[0]
    return jsonify(follower.to_dict())

@app.route('/followers/<int:id>', methods=['DELETE'])
def delete_follower_relationship(id):
    followers = Crud.read(Follower, filters={"id": id})
    if not followers:
        return jsonify({'error': 'Follower relationship not found'}), 404
    follower = followers[0]
    Crud.delete(follower)
    return jsonify({'message': 'Follower relationship deleted successfully'}), 204

@app.route('/followers/user/<int:user_id>', methods=['GET'])
def get_all_followers(user_id):
    followers = Crud.read(Follower, filters={"user_id": user_id})
    return jsonify([follower.to_dict() for follower in followers])

@app.route('/followers/follows/<int:user_id>', methods=['GET'])
def get_all_follows(user_id):
    follows = Crud.read(Follower, filters={"follower_id": user_id})
    return jsonify([follow.to_dict() for follow in follows])

@app.route('/followers/batch/add', methods=['POST'])
def batch_add_followers():
    data = request.get_json()
    followers = [Follower(user_id=data["user_id"], follower_id=f_id) for f_id in data["follower_ids"]]
    Crud.create_batch(Follower, followers)
    return jsonify({'message': 'Followers added successfully'}), 201

@app.route('/followers/batch/delete', methods=['POST'])
def batch_delete_followers():
    data = request.get_json()
    Crud.delete_batch(Follower, filters={"user_id": data["user_id"], "follower_id": data["follower_ids"]})
    return jsonify({'message': 'Followers deleted successfully'}), 204

# Export user profile
@app.route('/profile/<int:id>', methods=['GET'])
def generate_pdf(id):
    users = Crud.read(User, filters={"id": id})

    if not users:
        return jsonify({'error': 'User not found'}), 404

    user = users[0]
    user_role = Crud.read(UserRole, filters={"id": user.role_id})[0]
    user_experiences = Crud.read(UserExperience, filters={"user_id": id})

    # Render template and generate pdf
    html = render_template('template/profile.html', user=user, role=user_role, experiences=user_experiences)

    # Save pdf to a file
    pdf_path = f"profile_{id}.pdf"
    pdfkit.from_string(html, pdf_path)

    # Send the pdf file with Flask send_file
    response = send_file(pdf_path, mimetype='application/pdf', as_attachment=True)

    # Set the file name for the downloaded file
    response.headers["Content-Disposition"] = f"attachment; filename=profile_{id}.pdf"

    # Remove the pdf file after sending it
    os.remove(pdf_path)

    return response

# Save images to local folder
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if file and allowed_file(file.filename):
        # Get only the file extension
        _, ext = os.path.splitext(file.filename)

        # Generate a unique name using a UUID
        unique_filename = f"{uuid4()}{ext}"

        # Make directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Save file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        # Get the URL of the uploaded image for front-end display
        file_url = request.host_url + 'uploads/' + unique_filename

        return jsonify({'file_url': file_url}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on('join')
def on_join(data):
    user_id = data['user_id']
    socketio.join_room(user_id)

@app.route('/messages', methods=['POST'])
@handle_error
def send_message():
    data = request.get_json()
    message = Message(sender_id=data['sender_id'], receiver_id=data['receiver_id'], content=data['message'])
    result = Crud.create(message, check_foreign_keys={"Users": data["sender_id"], "Users": data["receiver_id"]})
    if 'error' in result:
        return result
    # Emit the message to the receiver
    socketio.emit('message', {'data': message.to_dict()}, room=data['receiver_id'])
    # Emit a response to the sender
    socketio.emit('message', {'data': message.to_dict(), 'status': 'sent'}, room=data['sender_id'])

    return jsonify({'message': 'Message sent successfully'}), 200

@app.route('/messages/<int:user_id>/<int:other_user_id>', methods=['GET'])
@handle_error
def get_messages(user_id, other_user_id):
    messages = Crud.read(
        Message,
        filters={
            "sender_id": [user_id, other_user_id],
            "receiver_id": [user_id, other_user_id]
        }
    )
    if 'error' in messages:
        return messages
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/conversations/<int:user_id>', methods=['GET'])
@handle_error
def get_conversations(user_id):
    conversations = Crud.read(
        Message,
        filters={
            "sender_id": user_id,
            "receiver_id": user_id
        }
    )
    if 'error' in conversations:
        return conversations
    return jsonify([conversation.to_dict() for conversation in conversations]), 200

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app)