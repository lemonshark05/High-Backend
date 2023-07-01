from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class UserRole(db.Model):
    __tablename__ = 'UserRoles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=False)


class Blog(db.Model):
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


class Comment(db.Model):
    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, ForeignKey('Blogs.id'))
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    blog = relationship('Blog', backref='comments')
    user = relationship('User', backref='comments')


class Scholarship(db.Model):
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


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    loginemail = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
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

class UserExperience(db.Model):
    __tablename__ = 'UserExperiences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=False)

    user = relationship('User', backref='user_experiences')


class Follower(db.Model):
    __tablename__ = 'Followers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    follower_id = db.Column(db.Integer, ForeignKey('Users.id'))

    user = relationship('User', backref='followers', foreign_keys=[user_id])
    follower = relationship('User', backref='following', foreign_keys=[follower_id])


class UserImage(db.Model):
    __tablename__ = 'UserImages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    image_url = db.Column(db.String(255))

    user = relationship('User', backref='user_images')


class UserVideo(db.Model):
    __tablename__ = 'UserVideos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    video_url = db.Column(db.String(255))

    user = relationship('User', backref='user_videos')


class University(db.Model):
    __tablename__ = 'Universities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text)
    official_link = db.Column(db.String(255))
    intro_image_url = db.Column(db.String(255))
    thumbnail_url = db.Column(db.String(255))
    scholarships_link = db.Column(db.String(255))


class AthleteType(db.Model):
    __tablename__ = 'AthleteTypes'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
