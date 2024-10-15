from App.models import Review, Student, User
from App.database import db



#add review to a specific student
def add_review(student_id, staff_id, review_text, rating):
    student = Student.query.get(student_id)
    staff = User.query.get(staff_id)

    if not student:
        return {"message": "Student not found."}
    if not staff:
        return {"message": "Staff not found."}

    new_review = Review(student_id=student_id, staff_id=staff_id, review_text=review_text, rating=rating)
    db.session.add(new_review)
    db.session.commit()
    return {"message": f"Review added successfully"}

#view reviews for a particular student
def view_student_reviews(student_id):
    student = Student.query.get(student_id)
    if not student:
        return {"message": "Student not found."}

    reviews = Review.query.filter_by(student_id=student_id).all()
    if not reviews:
        return {"message": "No reviews found for this student."}

    review_list = [review.get_json() for review in reviews]
    return {"reviews": review_list}