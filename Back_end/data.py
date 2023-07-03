from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask import jsonify
from sqlalchemy import inspect

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class UserRole(Base):
    __tablename__ = 'UserRoles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=False)


class Blog(Base):
    __tablename__ = 'Blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('Users.id'))
    type = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    author = relationship('User', backref='blogs')


class Comment(Base):
    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, ForeignKey('Blogs.id'))
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    blog = relationship('Blog', backref='comments')
    user = relationship('User', backref='comments')


class Scholarship(Base):
    __tablename__ = 'Scholarships'

    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, ForeignKey('Universities.id'))
    type = db.Column(db.String(255))
    description = db.Column(db.Text)
    application_link = db.Column(db.String(255))
    prize = db.Column(db.Numeric(10, 2))
    country = db.Column(db.String(255))
    success_rate = db.Column(db.Numeric(5, 2))
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    created_by = db.Column(db.Integer, ForeignKey('UserRoles.id'))

    university = relationship('University', backref='scholarships')
    creator = relationship('UserRole', backref='scholarships')


class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    loginemail = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))
    role_id = db.Column(db.Integer, ForeignKey('UserRoles.id'))
    profile_image = db.Column(db.String(255))
    community_page_url = db.Column(db.String(255))
    profile_visibility = db.Column(db.Boolean, default=False)
    time_zone = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    personal_info = db.Column(db.Text)
    is_visible_to_all_members = db.Column(db.Boolean, default=False)
    linkedin_link = db.Column(db.String(255))
    other_links = db.Column(JSONB)
    about_me = db.Column(db.Text)
    interested_in_coaches = db.Column(JSONB)
    interested_in_athletes = db.Column(JSONB)

    role = relationship('UserRole', backref='users')

class UserExperience(Base):
    __tablename__ = 'UserExperiences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)

    user = relationship('User', backref='user_experiences')


class Follower(Base):
    __tablename__ = 'Followers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    follower_id = db.Column(db.Integer, ForeignKey('Users.id'))

    user = relationship('User', backref='followers', foreign_keys=[user_id])
    follower = relationship('User', backref='following', foreign_keys=[follower_id])


class UserImage(Base):
    __tablename__ = 'UserImages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    image_url = db.Column(db.String(255))

    user = relationship('User', backref='user_images')


class UserVideo(Base):
    __tablename__ = 'UserVideos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    video_url = db.Column(db.String(255))

    user = relationship('User', backref='user_videos')


class University(Base):
    __tablename__ = 'Universities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text)
    official_link = db.Column(db.String(255))
    intro_image_url = db.Column(db.String(255))
    thumbnail_url = db.Column(db.String(255))
    scholarships_link = db.Column(db.String(255))


class AthleteType(Base):
    __tablename__ = 'AthleteTypes'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    wrapper.__name__ = func.__name__
    return wrapper

class Crud:
    @staticmethod
    def create(model_instance):
        try:
            db.session.add(model_instance)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def read(model, filters=None, order_by=None, page=None, per_page=None):
        try:
            query = model.query

            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        query = query.filter(getattr(model, key).in_(value))
                    else:
                        query = query.filter(getattr(model, key) == value)

            if order_by:
                for order in order_by:
                    if order.startswith('-'):
                        query = query.order_by(getattr(model, order[1:]).desc())
                    else:
                        query = query.order_by(getattr(model, order).asc())

            if page and per_page:
                pagination = query.paginate(page=page, per_page=per_page, error_out=False)
                items = pagination.items
            else:
                items = query.all()

            return items
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def join(model1, model2, join_type='inner', on=None, filters=None):
        try:
            if join_type.lower() == 'inner':
                query = db.session.query(model1).join(model2, on)
            elif join_type.lower() == 'left':
                query = db.session.query(model1).outerjoin(model2, on)
            else:
                raise ValueError('Invalid join type')

            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        query = query.filter(getattr(model1, key).in_(value))
                    else:
                        query = query.filter(getattr(model1, key) == value)

            return query.all()
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def update(model_instance, **kwargs):
        try:
            for attr, value in kwargs.items():
                if hasattr(model_instance, attr):
                    setattr(model_instance, attr, value)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def delete(model_instance):
        try:
            db.session.delete(model_instance)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def create_batch(model, instances):
        try:
            db.session.bulk_save_objects(instances)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def delete_batch(model, filters=None):
        try:
            query = model.query
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        query = query.filter(getattr(model, key).in_(value))
                    else:
                        query = query.filter(getattr(model, key) == value)
            query.delete()
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400

    @staticmethod
    def execute_raw(query, params=None):
        try:
            result = db.engine.execute(query, params)
            return result
        except SQLAlchemyError as e:
            return jsonify(error=str(e)), 400