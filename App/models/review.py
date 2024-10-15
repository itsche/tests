from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    staff = db.relationship('User', backref='reviews')

    def __init__(self, student_id, staff_id, review_text, rating):
        self.student_id = student_id
        self.staff_id = staff_id
        self.review_text = review_text
        self.rating = rating

    def get_json(self):
        staff_username = self.staff.username
        return {
            'review_text': self.review_text,
            'rating': self.rating,
            'staff_username': staff_username
        }