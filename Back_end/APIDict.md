# High-Backend API Design

## Table of Contents

- [Blogs API](#blogs-api)
  - [Create a new blog](#create-a-new-blog)
  - [Get a single blog](#get-a-single-blog)
  - [Get all blogs](#get-all-blogs)
  - [Get limited blogs](#get-limited-blogs)
  - [Update a blog](#update-a-blog)
  - [Delete a blog](#delete-a-blog)

- [University API](#university-api)
  - [Create a new university](#create-a-new-university)
  - [Get a single university](#get-a-single-university)
  - [Get all universities](#get-all-universities)
  - [Get limited universities](#get-limited-universities)
  - [Update a university](#update-a-university)
  - [Delete a university](#delete-a-university)

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

## University API

### Create a new university

**URL** : `http://localhost:8099/universities`

**Method** : `POST`

**Data constraints**

```json
{
    "name": "Harvard",
    "details": "Harvard University is ...",
    "official_link": "https://www.harvard.edu",
    "intro_image_url": "https://path-to-image.com/harvard.jpg",
    "thumbnail_url": "https://path-to-image.com/harvard-thumbnail.jpg",
    "scholarships_link": "https://www.harvard.edu/scholarships"
}
```

### Get a single university

Retrieve the details of a specific university by id.

**URL** : `http://localhost:8099/universities/{{university_id}}`

**Method** : `GET`

### Get all universities

Retrieve the details of all universities.

**URL** : `http://localhost:8099/universities`

**Method** : `GET`

### Get limited universities

Retrieve a limited number of universities.

**URL** : `http://localhost:8099/universities?limit={{limit}}`

**Method** : `GET`

### Update a university

Update the details of a specific university by id.

**URL** : `http://localhost:8099/universities/{{university_id}}`

**Method** : `PUT`

**Data constraints**

```json
{
    "name": "Harvard",
    "details": "Updated details ...",
    "official_link": "https://www.harvard.edu",
    "intro_image_url": "https://path-to-image.com/harvard.jpg",
    "thumbnail_url": "https://path-to-image.com/harvard-thumbnail.jpg",
    "scholarships_link": "https://www.harvard.edu/scholarships"
}
```

### Delete a university

Delete a specific university by id.

**URL** : `http://localhost:8099/universities/{{university_id}}`

**Method** : `DELETE`

Please replace `{{...}}` with the actual values.