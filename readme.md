Student Achievement Management System API Documentation
Authentication
All endpoints except /register and /login require a JWT token in the Authorization header.
Endpoints
User Management
Register User
Endpoint: /register
Method: POST
Body: { "name": "John Doe", "email": "john@example.com", "password": "secure123", "role": "Student", "linked_student_id": 1 }
Login
Endpoint: /login
Method: POST
Body: { "email": "john@example.com", "password": "secure123" }
Student Achievements
Add Student Achievement
Endpoint: /student-achievement
Method: POST
Body: { "linked_student_id": 2, "achievements": ["Won first place in the Science Fair", "Achieved perfect attendance for the semester", "Selected as team captain for the school's debate team"] }
Update Student Achievement
Endpoint: /student-achievement/{achievement_id}
Method: PUT
Body: { "achievement": "Won first place in National Science Fair 2025" }
Delete Student Achievement
Endpoint: /student-achievement/{achievement_id}
Method: DELETE
Body: None
Get Student Achievement
Endpoint: /student-achievement/{linked_student_id}
Method: GET
Body: None
Dashboards
Student Dashboard
Endpoint: /student_dashboard
Method: GET
Body: None
Note: Requires JWT token
School Dashboard
Endpoint: /school_dashboard
Method: GET
Body: None
Note: Requires JWT token
Note: Replace {achievement_id} and {linked_student_id} with actual IDs when making reuests.
