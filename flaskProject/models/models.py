from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

# Create the SQLAlchemy database object for use in app
db = SQLAlchemy()

# Class used to create the student and invoice database tables.


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.String(8), unique=True)
    hasOutstandingBalance = db.Column(db.Boolean, default=False)
    invoices = db.relationship(
        "Invoice", backref="student", cascade="all, delete-orphan"
    )
    # Delete orphan invoices if student is deleted.


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(8), unique=True)
    amount = db.Column(db.Float)
    dueDate = db.Column(db.Date)
    studentId = db.Column(
        db.String(8),
        db.ForeignKey(
            "student.studentId", ondelete="CASCADE", name="fk_invoice_student"
        ),
    )
    # Foreign key for invoices, to identify associated student.
    type = db.Column(db.String(15))
    status = db.Column(db.String(15), default="OUTSTANDING")
