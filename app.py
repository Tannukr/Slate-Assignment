from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, StudentAchievement
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret"
app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
app.config["JWT_VERIFY_SUB"] = False

jwt = JWTManager(app)
db.init_app(app)


@app.route("/register", methods=["POST"])
def register():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    role = request.json.get("role")
    linked_student_id = request.json.get("linked_student_id")

    if not all([name, email, password, role]):
        return jsonify({"error": "Missing required fields"}), 400
    
    if role == "Parent":
        student = User.query.filter_by(role="Student", linked_student_id=linked_student_id).first()
        if not student:
            return jsonify({"error": "Invalid linked Student ID"}), 404
    if email and User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    if role == "Student":
        if not linked_student_id:
            return jsonify({"error": "Linked Student ID is required"}), 400
        if User.query.filter_by(role="Student", linked_student_id=linked_student_id).first():
            return jsonify({"error": "This linked student ID is already registered"}), 409

    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role=role,
        linked_student_id=linked_student_id if role in ["Parent", "Student"] else None
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "role": role,
        "linked_student_id": linked_student_id if role in ["Parent", "Student"] else None
    }), 201

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        
        if not all([email, password]):
            return jsonify({"error": "Missing required fields"}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user_id": user.id,
            "role": user.role
        }), 200
    
    return jsonify({"error": "Invalid request method"}), 405

@app.route("/student-achievement", methods=["POST"])
@jwt_required()
def student_achievement():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if user.role != "School":
        return jsonify({"error": "Unauthorized. Only schools can add achievements"}), 403
    
    linked_student_id = request.json.get("linked_student_id")
    achievements = request.json.get("achievements")

    if not all([achievements, linked_student_id]) or not isinstance(achievements, list):
        return jsonify({"error": "Missing required fields or invalid format"}), 400
    
    student = User.query.filter_by(linked_student_id=linked_student_id, role="Student").first()

    if not student:
        return jsonify({"error": f"No student found with ID {linked_student_id}"}), 404

    new_achievements = []
    try:
        for achievement in achievements:
            new_achievement = StudentAchievement(
                linked_student_id=student.linked_student_id,
                school_name=user.name,
                achievement=achievement
            )
            db.session.add(new_achievement)
            new_achievements.append(new_achievement)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "Achievements added successfully",
        "student_id": linked_student_id,
        "achievements": [a.achievement for a in new_achievements]
    }), 201


@app.route("/student-achievements", methods=["GET"])
@jwt_required()
def get_student_achievements():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.role == "School":
        students = User.query.filter_by(role="Student").all()
    else:
        return jsonify({"error": "Unauthorized"}), 403
    results = []
    for student in students:
        achievements = StudentAchievement.query.filter_by(linked_student_id = student.id).all()
        student_info = {
            "linked_student_id": student.linked_student_id,
            # "student_id": student.id,
            "student_name": student.name,
            "school_name": achievements[0].school_name if achievements else None,
            "achievements": [achievement.achievement for achievement in achievements],

        }
        results.append(student_info)
    return jsonify(results), 200


@app.route("/student-achievement/<int:achievement_id>", methods=["DELETE"])
@jwt_required()
def delete_student_achievement(achievement_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if not user or user.role != "School":
        return jsonify({"error": "Unauthorized. Only schools can delete achievements"}), 403

    achievement = db.session.get(StudentAchievement, achievement_id)
    if not achievement:
        return jsonify({"error": "Achievement not found"}), 404

    try:
        db.session.delete(achievement)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete achievement: {str(e)}"}), 500

    return jsonify({
        "message": "Achievement deleted successfully",
        "achievement_id": achievement_id
    }), 200

@app.route("/student-achievement/<int:achievement_id>", methods=["PUT"])
@jwt_required()
def update_student_achievement(achievement_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if not user or user.role != "School":
        return jsonify({"error": "Unauthorized. Only schools can update achievements"}), 403

    new_achievement = request.json.get("achievement")
    if not new_achievement:
        return jsonify({"error": "Missing required fields"}), 400

    achievement = db.session.get(StudentAchievement, achievement_id)
    if not achievement:
        return jsonify({"error": "Achievement not found"}), 404

    achievement.achievement = new_achievement
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update achievement: {str(e)}"}), 500

    return jsonify({
        "message": "Achievement updated successfully",
        "achievement_id": achievement_id,
        "achievement": achievement.achievement
    }), 200


@app.route("/student_dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.role not in ["Student", "Parent"]:
        return jsonify({"error": "Unauthorized. Only students and parents can access this dashboard"}), 403
    
    if user.role == "Parent":
        student = User.query.filter_by(linked_student_id=user.linked_student_id, role="Student").first()
        if not student:
            return jsonify({"error": f"Student with linked ID {user.linked_student_id} not found"}), 404
        student_name = student.name
        student_id = student.linked_student_id
    else:
        student_name = user.name
        student_id = user.linked_student_id if user.linked_student_id else user.id
    
    achievements = StudentAchievement.query.filter_by(linked_student_id=student_id).all()
    
    if not achievements:
        return jsonify({
            "student_name": student_name,
            "student_id": student_id,
            "message": "No achievements found",
            "achievements": []
        }), 200
    
    return jsonify({
        "student_name": student_name,
        "linked_student_id": student_id,
        "school_name": achievements[0].school_name if achievements else None,
        "achievements": [achievement.achievement for achievement in achievements]
    }), 200



with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True)