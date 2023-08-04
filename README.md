# High-Backend

## Table of Contents
1. [Overview](#Overview)
2. [Prototype](#Prototype)
3. [Product Spec](#Product-Spec)
4. [PostgreSQL](#PostgreSQL)
5. [Postman](#Postman)

## Overview
### Description

### XMind
<img width="1065" alt="01" src="https://github.com/lemonshark05/High-Backend/assets/100770743/2e0bdb60-9505-4702-8ca1-e192eb7a0420">

## Prototype

### Draw
<img width="746" alt="Screenshot 2023-06-16 at 11 17 59" src="https://github.com/lemonshark05/High-Backend/assets/100770743/c18ae7db-a5b0-4426-b8b9-dca6f939ae68">
<img width="746" alt="Screenshot 2023-06-16 at 11 17 52" src="https://github.com/lemonshark05/High-Backend/assets/100770743/3bf1acbc-f830-4b8b-ad56-cc113a9284f7">


### Video

https://github.com/lemonshark05/High-Backend/assets/100770743/2e4a37d7-41e9-4c9e-a489-b399b1ae5c06

https://github.com/lemonshark05/High-Backend/assets/100770743/a02d372e-76fb-466b-bdc7-d0f6663877b3

## Website Spec

### 1. User Profile

* `UserRoles`: Defines the various roles within the application such as "Athlete", "Coach", and "Administrator".
* `Users`: Contains the user's basic profile data, including username, email, phone number, role, profile image, community page URL, profile visibility, timezone, display name, title, personal info, and visibility to all members. It also contains a user's LinkedIn-style bio, past experiences, and other relevant information.
* `Followers`: Allows for tracking follower relationships between users, similar to LinkedIn's connection system.
* `Subscriptions`: Contains any subscription details related to the user.

### 2. Screen Archetypes

* Login/Register
   * User can create an account
   * User can log in
   * User can sign up
* User Profile
    * User can view and edit their own profile with all existing posts, images, and reviews
        * Detailed Posts Page
        * Images Only Page
        * Endorsements and Recommendations
* Coach Profile
    * Users can view coach profiles, including posts by other users and average star rating
    * Users can endorse or recommend a coach
* Community Page
    * Users can interact with the community by viewing shared content, commenting, and liking posts

### 3. Navigation

**Tab Navigation** (Tab to Screen)

* Home
* Explore
* Resources
* Connection
* Me (User Profile)

**Flow Navigation** (Screen to Screen)

* Login/Register
   * Home Feed
* Home Feed
   * Coach Profile or User Profile
* User Profile
    * Settings
    * Profile Edit
    * My Network (Followers and Following)
    * Wallet
    * Addresses
    * Role (UserRoles)
    * My Posts
    * My Bookmarks
* My Network
    * Search for connections
    * View connection's profile
* Scholarships
    * Search for scholarships
    * View scholarship details
    * Apply for a scholarship
* Messaging
    * Compose message
    * View message thread
* Notifications
    * View notification details
* Me (User Profile)
    * Edit profile
    * View My posts
    * View My bookmarks
    * View and edit settings

## PostgreSQL
<img width="655" alt="Screenshot 2023-07-30 at 12 32 13" src="https://github.com/lemonshark05/High-Backend/assets/100770743/ba3c5346-a8f6-4d80-9e35-623da8286dca">
https://dbdiagram.io/d/649a3f9a02bd1c4a5e1ae74c

### Details
**Table: Blogs**

| Column Name | Type                     | Description                             |
|-------------|--------------------------|-----------------------------------------|
| id          | SERIAL PRIMARY KEY       | Unique ID for the blog                  |
| title       | VARCHAR(255)             | Title of the blog                       |
| content     | TEXT                     | Content of the blog                     |
| author_id   | INT REFERENCES Users(id) | Author's User ID                        |
| type        | VARCHAR(255)             | Type of the blog                        |
| image_url   | VARCHAR(255)             | URL of the blog image                   |
| views_count | INT DEFAULT 0            | Views of this blog                      |
| likes_count | INT DEFAULT 0            | Likes of this blog                      |
| created_at  | TIMESTAMP DEFAULT now()  | Time when the blog was created          |
| updated_at  | TIMESTAMP DEFAULT now()  | Time when the blog was last updated     |

**Table: Comments**

| Column Name | Type                     | Description                         |
|-------------|--------------------------|-------------------------------------|
| id          | SERIAL PRIMARY KEY       | Unique ID for the comment           |
| blog_id     | INT REFERENCES Blogs(id) | ID of the blog                      |
| user_id     | INT REFERENCES Users(id) | ID of the user who commented        |
| comment     | TEXT                     | Comment text                        |
| created_at  | TIMESTAMP DEFAULT now()  | Time when the comment was created   |
| updated_at  | TIMESTAMP DEFAULT now()  | Time when the comment was updated   |

**Table: Scholarships**

| Column Name      | Type                     | Description                                      |
|------------------|--------------------------|--------------------------------------------------|
| id               | SERIAL PRIMARY KEY       | Unique ID for the scholarship                    |
| university_id    | INT REFERENCES Universities(id) | ID of the university                      |
| type             | VARCHAR(255)             | Type of the scholarship                          |
| description      | TEXT                     | Description of the scholarship                   |
| application_link | VARCHAR(255)             | Application link for the scholarship             |
| prize            | DECIMAL(10,2)            | Prize amount for the scholarship                 |
| country          | VARCHAR(255)             | Country of the scholarship                       |
| success_rate     | DECIMAL(5,2)             | Success rate of the scholarship                  |
| image_url        | VARCHAR(255)             | Image URL of the scholarship                     |
| video_url        | VARCHAR(255)             | Video URL of the scholarship                     |
| created_id       | INT REFERENCES Users(id) | ID of the user who created the scholarship record|

**Table: Users**

| Column Name                | Type              | Description                                  |
|----------------------------|-------------------|----------------------------------------------|
| id                         | SERIAL PRIMARY KEY| Unique ID for the user                       |
| username                   | VARCHAR(255) UNIQUE NOT NULL | User's username                        |
| password                   | VARCHAR(255) NOT NULL | User's password                          |
| firstname                  | VARCHAR(255)      | User's first name                            |
| lastname                   | VARCHAR(255)      | User's last name                             |
| birthday                   | DATE              | User's birthday                              |
| email                      | VARCHAR(255) UNIQUE NOT NULL | User's email                          |
| role                       | VARCHAR(255) NOT NULL | User's role                               |
| phone                      | VARCHAR(255)      | User's phone number                          |
| avatar_url                 | VARCHAR(255)      | URL of the user's avatar                     |
| profile_image              | VARCHAR(255)      | URL of the user's profile image               |
| community_page_url         | VARCHAR(255)      | URL of the user's community page              |
| profile_visibility         | BOOLEAN DEFAULT false | Whether the user's profile is visible     |
| time_zone                  | VARCHAR(255)      | User's time zone                             |
| display_name               | VARCHAR(255)      | User's display name                          |
| education                  | TEXT              | User's education details                     |
| is_visible_to_all_members  | BOOLEAN DEFAULT false | Whether the user is visible to all members|
| other_links                | JSONB             | Other links related to the user               |
| about_me                   | TEXT              | Information about the user                    |
| interested_in_coaches      | JSONB             | Coaches the user is interested in            |
| interested_in_athletes     | JSONB             | Athletes the user is interested in           |

**Table: UserExperiences**

| Column Name  | Type                     | Description                                    |
|--------------|--------------------------|------------------------------------------------|
| id           | SERIAL PRIMARY KEY       | Unique ID for the experience                   |
| user_id      | INT REFERENCES Users(id) | ID of the user                                 |
| title        | VARCHAR(255)             | Title of the experience                        |
| description  | TEXT                     | Description of the experience                   |
| start_date   | DATE                     | Start date of the experience                   |
| end_date     | DATE                     | End date of the experience                     |
| is_current   | BOOLEAN DEFAULT false    | Whether the experience is current              |

**Table: Followers**

| Column Name  | Type                     | Description                                |
|--------------|--------------------------|--------------------------------------------|
| id           | SERIAL PRIMARY KEY       | Unique ID for the follower                 |
| user_id      | INT REFERENCES Users(id) | ID of the user                             |
| follower_id  | INT REFERENCES Users(id) | ID of the follower                         |

**Table: UserImages**

| Column Name  | Type                     | Description                                |
|--------------|--------------------------|--------------------------------------------|
| id           | SERIAL PRIMARY KEY       | Unique ID for the image                    |
| user_id      | INT REFERENCES Users(id) | ID of the user                             |
| image_url    | VARCHAR(255)             | URL of the image                           |

**Table: UserVideos**

| Column Name  | Type                     | Description                                |
|--------------|--------------------------|--------------------------------------------|
| id           | SERIAL PRIMARY KEY       | Unique ID for the video                    |
| user_id      | INT REFERENCES Users(id) | ID of the user                             |
| video_url    | VARCHAR(255)             | URL of the video                           |

**Table: Universities**

| Column Name       | Type            | Description                                |
|-------------------|-----------------|--------------------------------------------|
| id                | SERIAL PRIMARY KEY | Unique ID for the university            |
| name              | VARCHAR(255)      | Name of the university                    |
| details           | TEXT              | Details about the university              |
| official_link     | VARCHAR(255)      | Official link of the university           |
| intro_image_url   | VARCHAR(255)      | URL of the university's introductory image|
| thumbnail_url     | VARCHAR(255)      | URL of the university's thumbnail image   |
| scholarships_link | VARCHAR(255)      | Link to university's scholarships page    |

**Table: Messages**

| Column Name  | Type                     | Description                                |
|--------------|--------------------------|--------------------------------------------|
| id           | SERIAL PRIMARY KEY       | Unique ID for the message                  |
| sender_id    | INT REFERENCES Users(id) | ID of the message sender                   |
| receiver_id  | INT REFERENCES Users(id) | ID of the message receiver                 |
| content      | TEXT                     | Content of the message                     |
| created_at   | TIMESTAMP DEFAULT now()  | Time when the message was created          |

## Postman
https://grey-sunset-457798.postman.co/workspace/Team-Workspace~9f18450a-889f-46e8-8c86-4725b41b6a4d/overview
<img width="749" alt="Screenshot 2023-07-05 at 15 49 59" src="https://github.com/lemonshark05/High-Backend/assets/100770743/6700df95-36ea-427b-a001-0df6b23b64aa">
Here's a table with http status codes and descriptions:

| Status Code | Description |
|-------------|-------------|
| 200 | OK: The request was successful. |
| 201 | Created: The request was successful, and a resource was created as a result. |
| 204 | No Content: The server successfully processed the request, but is not returning any content. |
| 301 | Moved Permanently: The URL of the requested resource has been changed permanently. |
| 302 | Found: The server has found a temporary redirection. |
| 400 | Bad Request: The server could not understand the request due to invalid syntax. |
| 401 | Unauthorized: The request requires user authentication. |
| 403 | Forbidden: The server understood the request, but is refusing to fulfill it. |
| 404 | Not Found: The server can't find the requested resource. |
| 405 | Method Not Allowed: The method specified in the request is not allowed. |
| 500 | Internal Server Error: The server encountered an unexpected condition. |
| 502 | Bad Gateway: The server received an invalid response from the upstream server. |
| 503 | Service Unavailable: The server is currently unavailable (because it is overloaded or down for maintenance). |
| 504 | Gateway Timeout: The server was acting as a gateway or proxy and did not receive a timely response from the upstream server. |
