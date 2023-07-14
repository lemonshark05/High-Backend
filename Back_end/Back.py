import json

from flask import Flask, redirect, url_for, request, jsonify, render_template, send_file
from data import db, Comment, User, Blog, UserRole, UserPassword, UserExperience, University, UserImage, UserVideo, \
    Scholarship, AthleteType, Crud, Follower
from werkzeug.utils import secure_filename
import os
import pdfkit
from sqlalchemy import or_
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

os.environ[
    'OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # (**deploy should delete this line)Solve the problem about http to https
app = Flask(__name__, template_folder='templates')
app.config.from_object('config.Config')
app.secret_key = "mysecretkey"  # Replace with your secret key

# Configure the Google OAuth2.0
google_blueprint = make_google_blueprint(
    client_id=app.config.get("GOOGLE_OAUTH_CLIENT_ID"),  # Get Client ID from Config
    client_secret=app.config.get("GOOGLE_OAUTH_CLIENT_SECRET"),  # Get Client Secret from Config
    scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
           "openid"]
)
app.register_blueprint(google_blueprint, url_prefix="/google_login")
# initialize
db.init_app(app)


# Google mail login API
@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        return "You are {email} on Google".format(email=resp.json()["email"])
    except TokenExpiredError:
        return redirect(url_for("google.login"))


# log in with username and password
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['password']
        records = Crud.read(UserPassword, filters={'username': name})
        record_dict = records[0].to_dict()
        if pwd != record_dict['password']:
            return render_template('error.html', text='Wrong Password!')
    return render_template('login.html')


@app.route("/register_account", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        repwd = request.form['repassword']
        print(username, email, pwd, repwd)
        if pwd != repwd:
            return render_template('error.html', text='Passwords are not the same!')
        user_pwd = UserPassword(username, pwd)
        Crud.create(user_pwd)
        user = User(username, email)
        Crud.create(user)
    return render_template('register_account.html')


@app.route("/register_interest")
def register_interest():
    data = request.get_json()
    users = Crud.read(User, filters={"username": data['username']})
    if not users:
        return jsonify({'error': 'User not found'}), 404
    user = users[0]
    coaches = data['coaches']
    coach_json = json.dumps(coaches)
    Crud.update(user, interested_in_coaches=coach_json)
    return redirect(url_for('register_moreinfo'))


@app.route("/register/moreinfo")
def register_moreinfo():
    data = request.get_json()
    users = Crud.read(User, filters={"username": data['username']})
    if not users:
        return jsonify({'error': 'User not found'}), 404
    user = users[0]
    Crud.update(user, display_name=data['display_name'], title=data['title'], about_me=data['about_me'])
    return jsonify({'message': 'Register successfully!'}), 204


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


# Follower and Follow
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

    # Render templates and generate pdf
    html = render_template('profile.html', user=user, role=user_role, experiences=user_experiences)

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


# Save images to Google Drive
gauth = GoogleAuth(settings_file='client_secret.json')
gauth.scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

drive = GoogleDrive(gauth)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    # check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Save file to disk
        local_file_path = os.path.join("/tmp", filename)
        file.save(local_file_path)

        # Create & upload a file
        uploaded_file = drive.CreateFile({'title': filename})
        uploaded_file.SetContentFile(local_file_path)
        uploaded_file.Upload()

        # The ID of the file on Google Drive
        file_id = uploaded_file['id']

        # The URL where the image is stored on Google Drive
        file_url = f"https://drive.google.com/uc?export=view&id={file_id}"

        return jsonify({'file_url': file_url}), 200


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
