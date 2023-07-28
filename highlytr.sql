CREATE TABLE "Blogs" (
  "id" serial PRIMARY KEY,
  "title" varchar(255),
  "content" text,
  "author_id" int,
  "type" varchar(255),
  "image_url" varchar(255),
  "views_count" int DEFAULT 0,
  "likes_count" int DEFAULT 0,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "Comments" (
  "id" serial PRIMARY KEY,
  "blog_id" int,
  "user_id" int,
  "comment" text,
  "created_at" timestamp DEFAULT (now()),
  "updated_at" timestamp DEFAULT (now())
);

CREATE TABLE "Scholarships" (
  "id" serial PRIMARY KEY,
  "university_id" int,
  "type" varchar(255),
  "description" text,
  "application_link" varchar(255),
  "prize" decimal(10,2),
  "country" varchar(255),
  "success_rate" decimal(5,2),
  "image_url" varchar(255),
  "video_url" varchar(255),
  "created_id" int
);

CREATE TABLE "Users" (
  "id" serial PRIMARY KEY,
  "username" varchar(255) UNIQUE NOT NULL,
  "password" varchar(255) NOT NULL,
  "firstname" varchar(255),
  "lastname" varchar(255),
  "birthday" date,
  "email" varchar(255) UNIQUE NOT NULL,
  "role" varchar(255) NOT NULL,
  "phone" varchar(255),
  "avatar_url" varchar(255),
  "profile_image" varchar(255),
  "community_page_url" varchar(255),
  "profile_visibility" boolean DEFAULT false,
  "time_zone" varchar(255),
  "display_name" varchar(255),
  "education" text,
  "is_visible_to_all_members" boolean DEFAULT false,
  "other_links" jsonb,
  "about_me" text,
  "interested_in_coaches" jsonb,
  "interested_in_athletes" jsonb
);

CREATE TABLE "UserExperiences" (
  "id" serial PRIMARY KEY,
  "user_id" int,
  "title" varchar(255),
  "description" text,
  "start_date" date,
  "end_date" date,
  "is_current" boolean DEFAULT false
);

CREATE TABLE "Followers" (
  "id" serial PRIMARY KEY,
  "user_id" int,
  "follower_id" int
);

CREATE TABLE "UserImages" (
  "id" serial PRIMARY KEY,
  "user_id" int,
  "image_url" varchar(255)
);

CREATE TABLE "UserVideos" (
  "id" serial PRIMARY KEY,
  "user_id" int,
  "video_url" varchar(255)
);

CREATE TABLE "Universities" (
  "id" serial PRIMARY KEY,
  "name" varchar(255),
  "details" text,
  "official_link" varchar(255),
  "intro_image_url" varchar(255),
  "thumbnail_url" varchar(255),
  "scholarships_link" varchar(255)
);

CREATE TABLE "Messages" (
  "id" serial PRIMARY KEY,
  "sender_id" int,
  "receiver_id" int,
  "content" text,
  "created_at" timestamp DEFAULT (now())
);

ALTER TABLE "Blogs" ADD FOREIGN KEY ("author_id") REFERENCES "Users" ("id");

ALTER TABLE "Comments" ADD FOREIGN KEY ("blog_id") REFERENCES "Blogs" ("id");

ALTER TABLE "Comments" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Scholarships" ADD FOREIGN KEY ("university_id") REFERENCES "Universities" ("id");

ALTER TABLE "Scholarships" ADD FOREIGN KEY ("created_id") REFERENCES "Users" ("id");

ALTER TABLE "UserExperiences" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Followers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Followers" ADD FOREIGN KEY ("follower_id") REFERENCES "Users" ("id");

ALTER TABLE "UserImages" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UserVideos" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Messages" ADD FOREIGN KEY ("sender_id") REFERENCES "Users" ("id");

ALTER TABLE "Messages" ADD FOREIGN KEY ("receiver_id") REFERENCES "Users" ("id");
