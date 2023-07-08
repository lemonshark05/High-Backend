from flask import Flask, redirect, url_for, request, jsonify, render_template, send_file
from data import db, Comment, User, Blog, UserRole, UserExperience, University, UserImage, UserVideo, Scholarship, AthleteType, Crud
from werkzeug.utils import secure_filename
import os
from sqlalchemy import or_
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # (**deploy should delete this line)Solve the problem about http to https
app = Flask(__name__, template_folder='template')
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

if __name__ == '__main__':
    app.run(debug=True)
