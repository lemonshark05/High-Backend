from flask import Flask, redirect, url_for, request, jsonify, render_template, send_file
from data import db, Comment, User, Blog, UserRole, UserExperience, University, UserImage, UserVideo, Scholarship, AthleteType, Crud
from werkzeug.utils import secure_filename
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_dance.contrib.google import make_google_blueprint, google

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # (**deploy should delete this line)Solve the problem about http to https
app = Flask(__name__, template_folder='template')
app.config.from_object('config.Config')
app.secret_key = "mysecretkey"  # Replace with your secret key

# Configure the Google OAuth2.0
google_blueprint = make_google_blueprint(
    client_id=app.config.get("GOOGLE_OAUTH_CLIENT_ID"),  # Get Client ID from Config
    client_secret=app.config.get("GOOGLE_OAUTH_CLIENT_SECRET"),  # Get Client Secret from Config
    scope=["profile", "email"]
)
app.register_blueprint(google_blueprint, url_prefix="/google_login")
# initialize
db.init_app(app)

# Google mail login API
@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

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

@app.route('/blogs', methods=['GET'])
def get_all_blogs():
    blogs = Crud.read(Blog)
    return jsonify([blog.to_dict() for blog in blogs])

@app.route('/blogs', methods=['GET'])
def get_limited_blogs():
    # Get the page number (default 1 if not supplied)
    page = request.args.get('page', type=int, default=1)

    # Get the number of results per page (default 3 if not supplied)
    per_page = request.args.get('per_page', type=int, default=3)

    # Get filters if any
    filters = {}
    title = request.args.get('title')
    if title:
        filters['title'] = title
    author_id = request.args.get('author_id', type=int)
    if author_id:
        filters['author_id'] = author_id

    # Retrieve the blogs using the Crud.read method
    blogs = Crud.read(Blog, filters=filters, page=page, per_page=per_page)

    # Convert the blogs to dictionaries
    blogs_dict = [blog.to_dict() for blog in blogs.items]

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

@app.route('/universities', methods=['GET'])
def get_all_universities():
    universities = Crud.read(University)
    return jsonify([university.to_dict() for university in universities])

@app.route('/universities', methods=['GET'])
def get_limited_universities():
    limit = request.args.get('limit', type=int)
    universities = Crud.read(University).limit(limit)
    return jsonify([university.to_dict() for university in universities])

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
