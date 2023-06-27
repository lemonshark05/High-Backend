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


### App Evaluation
- **Category:** 
- **Story:** 
- **Market:**  
- **Habit:**  
- **Scope:**

## Prototype

### Draw
<img width="746" alt="Screenshot 2023-06-16 at 11 17 59" src="https://github.com/lemonshark05/High-Backend/assets/100770743/c18ae7db-a5b0-4426-b8b9-dca6f939ae68">
<img width="746" alt="Screenshot 2023-06-16 at 11 17 52" src="https://github.com/lemonshark05/High-Backend/assets/100770743/3bf1acbc-f830-4b8b-ad56-cc113a9284f7">


### Kap

https://github.com/lemonshark05/High-Backend/assets/100770743/2e4a37d7-41e9-4c9e-a489-b399b1ae5c06

https://github.com/lemonshark05/High-Backend/assets/100770743/a02d372e-76fb-466b-bdc7-d0f6663877b3

## Product Spec

### 1. User Profile

* `UserRoles`: Defines the various roles within the application such as "Athlete", "Coach", and "Administrator".
* `Users`: Contains the user's basic profile data, including username, email, phone number, role, profile image, community page URL, profile visibility, timezone, display name, title, personal info, and visibility to all members. It also contains a user's LinkedIn-style bio, past experiences, and other relevant information.
* `Followers`: Allows for tracking follower relationships between users, similar to LinkedIn's connection system.
* `BlockedMembers`: Tracks any blocked members for a particular user.
* `Subscriptions`: Contains any subscription details related to the user.
* `Orders`: Tracks any orders placed by the user.
* `Addresses`: Stores user's address details.
* `Wallet`: Holds information about the user's virtual wallet balance.
* `Bookings`: Contains any bookings made by the user.
* `UserUniversity`: Stores the association between users and their universities.

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
* Messaging 
    * Users can send and receive messages, allowing communication between coaches and athletes
* Connections
    * Users can send, accept, or decline connection requests
* Scholarship Opportunities
    * Users can view and apply for scholarship opportunities
    * Coaches can post scholarship opportunities

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

![Untitled](https://github.com/lemonshark05/High-Backend/assets/100770743/1baf3fec-e60e-4baf-b590-bf25ce778503)


**Table: UserRoles**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the role                   |
| role        | VARCHAR(255)      | Role name ("Athlete", "Coach", "Administrator") |
```

**Table: Blogs**
```
| Column Name  | Type                   | Description                  |
|--------------|------------------------|------------------------------|
| id           | SERIAL PRIMARY KEY     | Unique ID for the blog       |
| title        | VARCHAR(255)           | Title of the blog            |
| content      | TEXT                   | Content of the blog          |
| author_id    | INT REFERENCES Users(id)  | Author's User ID        |
| type         | VARCHAR(255)           | Type of the blog             |
| image_url    | VARCHAR(255)           | URL of the blog image        |
| created_at   | TIMESTAMP              | Time when the blog was created |
| updated_at   | TIMESTAMP              | Time when the blog was last updated |
```

**Table: Comments**
```
| Column Name | Type                  | Description                                |
|-------------|-----------------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY    | Unique ID for the comment                  |
| blog_id     | INT REFERENCES Blogs(id) | ID of the blog the comment belongs to |
| user_id     | INT REFERENCES Users(id) | User ID of the comment's author      |
| comment     | TEXT                  | The comment text                          |
| created_at  | TIMESTAMP             | Time when the comment was created         |
| updated_at  | TIMESTAMP             | Time when the comment was last updated    |
```

**Table: Scholarships**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the scholarship            |
| university_id | INT REFERENCES Universities(id) | University ID           |
| type        | VARCHAR(255)   | Type of scholarship (What kinds of athletes could apply) |
| description | TEXT           | Description of the scholarship             |
| application_link | VARCHAR(255) | URL of the application                   |
| prize       | DECIMAL(10,2)  | Prize of the scholarship                   |
| country     | VARCHAR(255)   | Country of the scholarship                 |
| success_rate | DECIMAL(5,2)   | Success rate of the scholarship           |
| image_url   | VARCHAR(255)   | URL of the scholarship image               |
| video_url   | VARCHAR(255)   | URL of the scholarship video               |
| created_by  | INT REFERENCES UserRoles(id) | Role ID of the creator (Admin or Coach) |
```
**Table: Users**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the user                   |
| username    | VARCHAR(255)      | User's username                           |
| email       | VARCHAR(255)      | Unique user's email                       |
| loginemail  | VARCHAR(255)      | Login email created at registration       |
| phone       | VARCHAR(255)      | User's phone number                       |
| role_id     | INT REFERENCES UserRoles(id) | Role ID                       |
| profile_image | VARCHAR(255) | URL of profile image                       |
| community_page_url | VARCHAR(255) | URL of community page                   |
| profile_visibility | BOOLEAN | Visibility status of profile               |
| time_zone   | VARCHAR(255)   | User's time zone                           |
| display_name | VARCHAR(255)  | User's display name                        |
| title       | VARCHAR(255)   | User's title                               |
| personal_info | TEXT | User's personal info                             |
| is_visible_to_all_members | BOOLEAN | Visibility to all members            |
| linkedin_link | VARCHAR(255) | Linkedin profile link                      |
| other_links | JSONB | JSONB array of other social links (Twitter, Facebook, etc.) |
| about_me    | TEXT | About me information                               |
| interested_in_coaches | JSONB | JSONB array of interested coach IDs      |
| interested_in_athletes | JSONB | JSONB array of interested athlete IDs    |
```
**Table: Followers**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the follower relationship |
| user_id     | INT REFERENCES Users(id) | User ID                           |
| follower_id | INT REFERENCES Users(id) | Follower's user ID                 |
```
**Table: UserImages**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the user image             |
| user_id     | INT REFERENCES Users(id) | User ID                           |
| image_url   | VARCHAR(255) | URL of user's image                         |
```
**Table: UserVideos**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the user video             |
| user_id     | INT REFERENCES Users(id) | User ID                           |
| video_url   | VARCHAR(255) | URL of user's video                         |
```
**Table: Universities**
```
| Column Name | Type            | Description                                  |
|-------------|-----------------|----------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the university               |
| name        | VARCHAR(255)   | University name                              |
| details     | TEXT | University details                                    |
| official_link | VARCHAR(255) | Official URL of the university               |
| intro_image_url | VARCHAR(255) | URL of introduction image of the university |
| thumbnail_url | VARCHAR(255) | URL of thumbnail image of the university     |
| scholarships_link | VARCHAR(255) | Link to the scholarships of the university |
```
**Table: AthleteTypes**
```
| Column Name | Type            | Description                                |
|-------------|-----------------|--------------------------------------------|
| id          | SERIAL PRIMARY KEY | Unique ID for the athlete type           |
| type        | VARCHAR(255)   | Athlete type name                          |
```

###  Digital Wireframes & Mockups


###  Interactive Prototype


## Postman
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


