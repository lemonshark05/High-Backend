import psycopg2

class User:
    def __init__(self, password, username, title, email):
        self.username = username
        self.password = password
        self.title = title
        self.email = email

class UserRole:
    def __init__(self, role):
        self.role = role

class Follower:
    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id

class BlockedMember:
    def __init__(self, user_id, blocked_user_id):
        self.user_id = user_id
        self.blocked_user_id = blocked_user_id

class Subscription:
    def __init__(self, user_id, subscription_details):
        self.user_id = user_id
        self.subscription_details = subscription_details

class Order:
    def __init__(self, user_id, order_details):
        self.user_id = user_id
        self.order_details = order_details

class Address:
    def __init__(self, user_id, address):
        self.user_id = user_id
        self.address = address

class Wallet:
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance

class Booking:
    def __init__(self, user_id, booking_details):
        self.user_id = user_id
        self.booking_details = booking_details

class Resource:
    def __init__(self, resource_type, resource_details):
        self.resource_type = resource_type
        self.resource_details = resource_details

class University:
    def __init__(self, name, details):
        self.name = name
        self.details = details

class UserUniversity:
    def __init__(self, user_id, university_id):
        self.user_id = user_id
        self.university_id = university_id

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)

# Create the UserRoles and Users tables
def create_tables():
    try:
        cursor = conn.cursor()

        # Create UserRoles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserRoles (
                id SERIAL PRIMARY KEY,
                role VARCHAR(255)
            )
        """)

        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(255),
                role_id INT REFERENCES UserRoles(id),
                profile_image VARCHAR(255),
                community_page_url VARCHAR(255),
                profile_visibility BOOLEAN,
                time_zone VARCHAR(255),
                display_name VARCHAR(255),
                title VARCHAR(255),
                personal_info TEXT,
                is_visible_to_all_members BOOLEAN
            )
        """)
        # Create Followers table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Followers (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        follower_id INT REFERENCES Users(id)
                    )
                """)

        # Create BlockedMembers table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS BlockedMembers (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        blocked_user_id INT REFERENCES Users(id)
                    )
                """)

        # Create Subscriptions table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Subscriptions (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        subscription_details TEXT
                    )
                """)

        # Create Orders table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Orders (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        order_details TEXT
                    )
                """)

        # Create Addresses table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Addresses (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        address TEXT
                    )
                """)

        # Create Wallet table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Wallet (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        balance DECIMAL(10,2)
                    )
                """)

        # Create Bookings table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Bookings (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        booking_details TEXT
                    )
                """)

        # Create Resources table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Resources (
                        id SERIAL PRIMARY KEY,
                        resource_type VARCHAR(255),
                        resource_details TEXT
                    )
                """)

        # Create Universities table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Universities (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        details TEXT
                    )
                """)

        # Create UserUniversity table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS UserUniversity (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Users(id),
                        university_id INT REFERENCES Universities(id)
                    )
                """)

        conn.commit()
        print("Tables created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error creating tables:", error)

    finally:
        if conn:
            cursor.close()
            conn.close()

# Call the create_tables function to create the tables
if __name__ == '__main__':
    create_tables()