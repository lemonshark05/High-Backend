from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from flask import Flask
from data import db, Comment

from data import User, Blog, UserRole, UserExperience, AthleteType, Crud, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5433/postgres'  # Replace with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

db.init_app(app)

def main():
    # Create Faker instance
    fake = Faker()

    with app.app_context():
        # Drop all tables and recreate them
        # db.drop_all()
        # db.create_all()

        # # Create UserRoles
        # roles = ['athlete', 'coach', 'admin']
        # for role in roles:
        #     Crud.create(UserRole(role=role))
        #
        # # Create AthleteTypes
        # types = ['football', 'basketball', 'volleyball', 'swim']
        # for type in types:
        #     Crud.create(AthleteType(type=type))

        # # Create Users
        # user_roles = Crud.read(UserRole)
        # users = []
        # for i, user_role in enumerate(user_roles, start=1):
        #     user = User(username=fake.user_name(), email=fake.email(), role_id=user_role.id)
        #     users.append(user)
        #     Crud.create(user)
        #
        # # Predefined titles related to sports
        # sports_related_titles = ['Athlete', 'Coach', 'Team Leader', 'Team Member']
        #
        # # Create UserExperiences
        # for user in users:
        #     for i in range(1, fake.random_int(min=1, max=3)):
        #         experience = UserExperience(user_id=user.id, title=fake.random_element(elements=sports_related_titles), description=fake.text(), start_date=fake.date_this_decade(), end_date=fake.date_this_decade(), is_current=fake.boolean())
        #         Crud.create(experience)
        #
        # # Create Blogs
        # sports_related_sentences = ['Amazing game last night', 'Unforgettable match', 'Incredible team performance', 'Outstanding individual effort', 'Heartbreaking loss']

        # for i in range(1, 6):
        #     blog = Blog(title=fake.random_element(elements=sports_related_sentences), content=fake.sentence(ext_word_list=sports_related_sentences), author_id=fake.random_element(elements=[user.id for user in users]))
        #     Crud.create(blog)
        # Get the users who will write the comments
        comment_authors = Crud.read(User, filters={"id": [1, 2, 3, 4, 5, 6]})

        # Create Comments for Blogs 1-3
        for blog_id in range(1, 14):
            for author in comment_authors:
                # Use Faker to generate some text for the comment
                comment_text = fake.sentence()
                comment = Comment(user_id=author.id, blog_id=blog_id, comment=comment_text)
                Crud.create(comment)

if __name__ == "__main__":
    main()
