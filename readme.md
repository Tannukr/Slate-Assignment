Student Achievements API

This is a Flask-based REST API for managing student achievements. It supports user authentication, role-based access control, and CRUD operations on student achievements.

Setup Instructions

Prerequisites

Python 3.8+

SQLite (default database)

Postman (for API testing)

Git (to clone the repository)

Installation

Clone the repository

git clone https://github.com/Tannukr/Student_achievement_System.git
cd student-achievements-api

Create and activate a virtual environment

python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate    # On Windows

Install dependencies

pip install -r requirements.txt

Run the application

python app.py

API Endpoints

Authentication

POST /register - Register a new user

POST /login - Authenticate and receive an access token

Student Achievements

POST /student-achievement - Add student achievements (requires authentication)

GET /student-achievements - Retrieve all student achievements

PUT /student-achievement/<id> - Update a specific achievement (requires authentication)

DELETE /student-achievement/<id> - Delete a specific achievement (requires authentication)

Testing with Postman

Import the provided Postman collection.

Use the login API to obtain a JWT token.

Add the token to your API requests in the Authorization header as Bearer <token>.
