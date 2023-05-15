from models.models import Student
from app import db


class StudentService:
    @staticmethod
    def create_student(student_id):
        """
        Creates a student from a given student ID and commits it to the database.

                    Parameters:
                    a (int): The student ID of a student to create.

                    Returns:
                        String containing success or failure information.
        """
        student = Student.query.filter_by(studentId=student_id).first()
        if student is not None:
            return "Student already exists"
        # Create a new student record
        new_student = Student(studentId=student_id)
        db.session.add(new_student)
        db.session.commit()
        return "Student created successfully"

    @staticmethod
    def get_student(student_id):
        """
        Gets student data object associated with the provided student ID.

        Parameters:
        a (int): The student ID to receive the object of.

        Returns:
        Student data object.
        """
        student = Student.query.filter_by(studentId=student_id).first()
        if not student:
            raise Exception(f"Student with ID {student_id} not found")

        return student

    @staticmethod
    def get_outstanding_references(student_id):
        """
        Gets references from all outstanding invoices associated with the provided student ID.

        Parameters:
        a (int): The student ID to receive references from.

        Returns:
        A list of all associated invoices that are outstanding.
        """
        student = StudentService.get_student(student_id)
        invoices = (
            student.invoices
        )  # Create reference to the student object and access all of its invoices.
        return [
            invoice.reference for invoice in invoices if invoice.status == "OUTSTANDING"
        ]

    @staticmethod
    def has_outstanding_balance(student_id):
        """
        Returns references from outstanding invoices associated with the provided student ID.

        Parameters:
        a (int): The student ID to receive references from.

        Returns:
        A list of all associated invoices that are outstanding.
        """
        student = StudentService.get_student(student_id)
        if student == 1:
            return True
        else:
            return False

    @staticmethod
    def check_student_exists(student_id):
        """
        Checks that a student already exists from a student ID.

        Parameters:
        a (int): The student ID to check.

        Returns:
        Boolean true or false, whether the student is already existent.
        """
        student = Student.query.filter_by(studentId=student_id).first()
        if student is None:
            StudentService.create_student(student_id)
            return False
        return True

    @staticmethod
    def update_outstanding_balance(student_id):
        """
        Updates whether a student has an outstanding balance or not.

        Parameters:
        a (int): The student ID to update outstanding balance.
        """
        student = StudentService.get_student(student_id)
        invoices = student.invoices
        if any(invoice.status == "OUTSTANDING" for invoice in invoices):
            # If any invoices have an outstanding balance, set outstanding balance to 1.
            if student.hasOutstandingBalance == 0:
                student.hasOutstandingBalance = 1
        else:
            student.hasOutstandingBalance = 0
        db.session.commit()  # Commit changes to the database.
