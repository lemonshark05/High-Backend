# High-Backend

## Table of Contents
1. [Overview](#Overview)
1. [Product Spec](#Product-Spec)
3. [PostgreSQL](#PostgreSQL)

## Overview
### Description

### App Evaluation
- **Category:** 
- **Mobile:**
- **Story:** 
- **Market:**  
- **Habit:**  
- **Scope:** 


## Product Spec

### 1. User Stories (Required and Optional)

**Required Must-have Stories**

* User can see people other user's images and ratings around the area
* User can build a profile

**Optional Nice-to-have Stories**

* Users can create 

### 2. Screen Archetypes

* Login/Resgister
   * User can create account
   * User can log in
* User Profile
    * User can see their own profile with all the existing reviews and images they have posted
        * Detailed Posts Page
        * Images Only Page
* Coach Profile
    * Users can see the restaurant's page with all the posts created by other users and the average star rating
* 
### 3. Navigation

**Tab Navigation** (Tab to Screen)

* Homepage
* Search (NTH)

**Flow Navigation** (Screen to Screen)

* Login/Register
   * Discover Feed
* Discover Feed
   * Restaurant Profile
* User Profile
    * Posts
    * Feed
    * Bookmarks
* Posting
    * Discover Feed

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



### This is not due until the following week: 
## Schema 


### Models
[Add table of models]
### Networking


