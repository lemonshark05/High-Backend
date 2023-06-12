# High-Backend

## Table of Contents
1. [Overview](#Overview)
2. [Product Spec](#Product-Spec)
3. [PostgreSQL](#PostgreSQL)
4. [Postman](#Postman)

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
* My Network (Connections and Followers)
* Scholarships
* Messaging
* Notifications
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
Certainly, here's the database schema:

**Table: UserRoles**

| Column Name | Type         | Description             |
|-------------|--------------|-------------------------|
| id          | INT PRIMARY KEY | Unique ID for the role |
| role        | VARCHAR(255)   | Role name ("Athlete", "Coach", "Administrator") | 

**Table: Users**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the user |
| username    | VARCHAR(255)   | User's username |
| email       | VARCHAR(255)   | Unique user's email |
| phone       | VARCHAR(255)   | User's phone number |
| role_id     | INT REFERENCES UserRoles(id) | Role ID |
| profile_image | VARCHAR(255) | URL of profile image |
| community_page_url | VARCHAR(255) | URL of community page |
| profile_visibility | BOOLEAN | Visibility status of profile |
| time_zone   | VARCHAR(255)   | User's time zone |
| display_name | VARCHAR(255)  | User's display name |
| title       | VARCHAR(255)   | User's title |
| personal_info | TEXT | User's personal info |
| is_visible_to_all_members | BOOLEAN | Visibility to all members |

**Table: Followers**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the follower relationship |
| user_id     | INT REFERENCES Users(id) | User ID |
| follower_id | INT REFERENCES Users(id) | Follower's user ID |

**Table: BlockedMembers**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the blocked member |
| user_id     | INT REFERENCES Users(id) | User ID |
| blocked_user_id | INT REFERENCES Users(id) | Blocked user's ID |

**Table: Subscriptions**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the subscription |
| user_id     | INT REFERENCES Users(id) | User ID |
| subscription_details | TEXT | Subscription details |

**Table: Orders**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the order |
| user_id     | INT REFERENCES Users(id) | User ID |
| order_details | TEXT | Order details |

**Table: Addresses**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the address |
| user_id     | INT REFERENCES Users(id) | User ID |
| address     | TEXT | Address details |

**Table: Wallet**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the wallet |
| user_id     | INT REFERENCES Users(id) | User ID |
| balance     | DECIMAL(10,2) | Wallet balance |

**Table: Bookings**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the booking |
| user_id     | INT REFERENCES Users(id) | User ID |
| booking_details | TEXT | Booking details |

**Table: Resources**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the resource |
| resource_type | VARCHAR(255) | Resource type ("basketball", "football", etc.) |
| resource_details | TEXT | Resource details |

**Table: Universities**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the university |
| name        | VARCHAR(255)   | University name |
| details     | TEXT | University details |

**Table: UserUniversity**

| Column Name | Type         | Description |
|-------------|--------------|-------------|
| id          | INT PRIMARY KEY | Unique ID for the user-university relationship |
| user_id     | INT REFERENCES Users(id) | User ID |
| university_id | INT REFERENCES Universities(id) | University ID |


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


