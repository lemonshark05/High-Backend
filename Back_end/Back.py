from flask import Flask, request, jsonify
from data import db, Comment, User, Blog, UserRole, UserExperience, University, UserImage, UserVideo, Scholarship, AthleteType, Crud

app = Flask(__name__)
app.config.from_object('config.Config')
# initialize
db.init_app(app)

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
    limit = request.args.get('limit', type=int)
    blogs = Crud.read(Blog).limit(limit)
    return jsonify([blog.to_dict() for blog in blogs])

@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.get_json()
    blog = Crud.read_by_id(Blog, blog_id)
    if blog is None:
        return jsonify({'error': 'Blog not found'}), 404
    Crud.update(blog, **data)
    return jsonify(blog.to_dict())

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Crud.read_by_id(Blog, blog_id)
    if blog is None:
        return jsonify({'error': 'Blog not found'}), 404
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
    university = Crud.read(University, filters={"id": university_id})
    if university is None:
        return jsonify({'error': 'University not found'}), 404
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
    university = Crud.read_by_id(University, university_id)
    if university is None:
        return jsonify({'error': 'University not found'}), 404
    Crud.update(university, **data)
    return jsonify(university.to_dict())

@app.route('/universities/<int:university_id>', methods=['DELETE'])
def delete_university(university_id):
    university = Crud.read_by_id(University, university_id)
    if university is None:
        return jsonify({'error': 'University not found'}), 404
    Crud.delete(university)
    return jsonify({'message': 'University deleted successfully'}), 204


if __name__ == '__main__':
    app.run(debug=True)
