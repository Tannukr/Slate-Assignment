Student Achievement Management System API Documentation
Register User
Endpoint: /register
Method: POST
json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secure123",
    "role": "Student",
    "linked_student_id": 1
}
Login
Endpoint: /login
Method: POST
json
{
    "email": "john@example.com",
    "password": "secure123"
}
Add Student Achievement
Endpoint: /student-achievement
Method: POST
json
{
    "linked_student_id": 2,
    "achievements": [
        "Won first place in the Science Fair",
        "Achieved perfect attendance for the semester",
        "Selected as team captain for the school's debate team"
    ]
}
Update Student Achievement
Endpoint: /student-achievement/{achievement_id}
Method: PUT
json
{
    "achievement": "Won first place in National Science Fair 2025"
}
Delete Student Achievement
Endpoint: /student-achievement/{achievement_id}
Method: DELETE
No request body needed
Replace {achievement_id} with actual ID
Get Student Achievement
Endpoint: /student-achievement/{linked_student_id}
Method: GET
No request body needed
Replace {linked_student_id} with actual ID
Student Dashboard
Endpoint: /student_dashboard
Method: GET
No request body needed
Requires JWT token
School Dashboard
Endpoint: /school_dashboard
Method: GET
No request body needed
Requires JWT token
Note: All endpoints except /register and /login require JWT token in Authorization header.