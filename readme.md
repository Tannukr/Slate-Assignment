# Student Achievement Management System

A Flask REST API for managing student achievements with role-based authentication (School, Parent, Student).

## Features
- JWT Authentication
- Role-based access control
- Student achievement management
- SQLite database
- Secure password handling

## Setup
1. Create virtual environment: `python -m venv env`
2. Activate environment: `env\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run application: `python app.py`

## API Endpoints
- POST /auth/register - User registration
- POST /auth/login - User login
- GET /student/achievements/{student_id} - View achievements
- POST /school/add-achievement - Add new achievement
