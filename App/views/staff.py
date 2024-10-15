from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import user, review, student
from App.database import db

from App.controllers.user import (
    create_user, get_user_by_username, get_user, get_all_users, get_all_users_json, update_user, toJSON
)

staff_views = Blueprint('staff_views', __name__)

@staff_views.route('/api/staff/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_staff(id):
    user = get_user(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@staff_views.route('/api/review', methods=['POST'])
@jwt_required()
def create_review():
    data = request.json
    staff_id = get_jwt_identity()
    student_id = data.get('student_id')
    content = data.get('content')
    if not student_id or not content:
        return jsonify({"error": "Student ID and content required"}), 400
    review = review(staff_id=staff_id, student_id=student_id, content=content)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201

@staff_views.route('/api/review/<int:id>', methods=['GET'])
@jwt_required()
def get_review(id):
    review = review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review.to_dict()), 200

@staff_views.route('/api/review', methods=['GET'])
@jwt_required()
def get_all_reviews():
    reviews = review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200

@staff_views.route('/api/review/<int:id>', methods=['PUT'])
@jwt_required()
def update_review(id):
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({"error": "Content required"}), 400
    review = review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    review.content = content
    db.session.commit()
    return jsonify(review.to_dict()), 200

@staff_views.route('/api/review/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = review.query.get(id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200

@staff_views.route('/api/student/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    student = student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200

@staff_views.route('/api/student', methods=['GET'])
@jwt_required()
def get_all_students():
    students = student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

@staff_views.route('/api/student/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name required"}), 400
    student = student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student.name = name
    db.session.commit()
    return jsonify(student.to_dict()), 200

@staff_views.route('/api/student/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    student = student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"}), 200