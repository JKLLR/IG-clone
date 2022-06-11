# IG-clone

## Description

 IG-clone is an instagram like application built with the aim of learning django. It allows users to post images, see other people's posts and comment.
## Author

[JeffHuria](https://github.com/JKLLR)

## Features


As a user of the application you will be able to:

1. See all posted photos
2. See each post's caption, location, caption and date posted.
3. Upload posts
4. Create profiles and edit profiles
5. Search for a post by username

## BDD
| Behavior            | Input                         | Output                        | 
| ------------------- | ----------------------------- | ----------------------------- |
| Login to admin  | **username**: moringa , **password** : moringa1234 | view and make changes to the admin | 
Signup to the application | Click on `Signup` | A sign up page appears with a sign up form |
|  Login to the site | Click on `Log in`  | Redirected to the login page with a login form |
|  Search in the search field | Input keywords to be searched then click SEARCH | Search page is loaded and displays with the searched results |
|Upload a post|click on `Post`| An upload page appears with an upload form containing different fields|
|View profile|click `Profile`|Redirects to profile page with an option to edit profile|


## Getting started
### Prerequisites
* python3.6
* virtual environment
* pipenv
* django 2.2.7
### Technologies
* BackEnd:
      * Python
      * Django
* FontEnd:
      * HTML
      * CSS
      * JavaScript
      * Bootstrap
* Database
      * PostgreSQL
* Deployment
      * Heroku   



## Installation
### Requirements

* Either a computer,phone,tablet or an Ipad
* An access to the Internet


### Installation
To get the code..

1. Cloning the repository:
  ```bash
  git clone https://github.com/JKLLR/IG-clone.git
  ```
2. Move to the folder and install requirements
  ```bash
  cd myapp
  pip install <package name>
  ```
3. Running the application

  ```bash
  make
  ```
4. Testing the application
  ```bash
  python3.8 manage.py test
  ```
Open the application on your browser `127.0.0.1:8000`.
### Known bugs
No known bugs

## Contact Information

For any further inquiries or contributions or comments, reach me at 
[JeffHuria](https://github.com/JKLLR)


### License

[MIT](license)

Copyright (c) 2022
