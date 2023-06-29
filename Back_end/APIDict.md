# High-Backend API Design

## Table of Contents

- [Blogs API](#blogs-api)
  - [Create a new blog](#create-a-new-blog)
  - [Get a single blog](#get-a-single-blog)
  - [Get all blogs](#get-all-blogs)
  - [Get limited blogs](#get-limited-blogs)
  - [Update a blog](#update-a-blog)
  - [Delete a blog](#delete-a-blog)

## Blogs API

### Create a new blog

**URL** : `http://localhost:8099/blogs`

**Method** : `POST`

**Data constraints**

```json
{
    "title": "Sample Blog",
    "content": "This is a sample blog post.",
    "author_id": "{{author_id}}",
    "type": "News",
    "comments_count": 0,
    "views_count": 0,
    "image_url": "https://path-to-image.com/blog.jpg"
}
```

### Get a single blog

Retrieve the details of a specific blog by id.

**URL** : `http://localhost:8099/blogs/{{blog_id}}`

**Method** : `GET`

### Get all blogs

Retrieve the details of all blogs.

**URL** : `http://localhost:8099/blogs`

**Method** : `GET`

### Get limited blogs

Retrieve a limited number of blogs.

**URL** : `http://localhost:8099/blogs?limit={{limit}}`

**Method** : `GET`

### Update a blog

Update the title and content of a specific blog by id.

**URL** : `http://localhost:8099/blogs/{{blog_id}}`

**Method** : `PUT`

**Data constraints**

```json
{
    "title": "Updated Blog",
    "content": "This is an updated blog post."
}
```

### Delete a blog

Delete a specific blog by id.

**URL** : `http://localhost:8099/blogs/{{blog_id}}`

**Method** : `DELETE`

Please replace `{{...}}` with the actual values.
