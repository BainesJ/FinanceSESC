from models.models import Invoice
from app import db
from datetime import date, timedelta
import random
import string
from models.models import Invoice
from services import studentService


class InvoiceService:
    student_service = studentService.StudentService()

    @staticmethod
    def generate_unique_reference():
        """
        Generates a unique 8 digit reference code of letters and numbers.

        Return:
        A unique 8 digit string of letters and numbers.
        """
        while True:
            reference = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            existing_invoice = Invoice.query.filter_by(reference=reference).first()
            if not existing_invoice:
                return reference

    @staticmethod
    def create_invoice(new_invoice):
        """
        Creates an invoice in the finance service, using an invoice object from another microservice.

        Parameters:
        a (Invoice): An invoice to store in the finance service.

        Return:
        The created invoice object.
        """
        invoice = Invoice(
            reference=InvoiceService.generate_unique_reference(),
            amount=new_invoice.get("amount"),
            dueDate=new_invoice.get("due"),
            type=new_invoice.get("type"),
            studentId=new_invoice.get("studentId"),
        )
        InvoiceService.student_service.check_student_exists(invoice.studentId)
        db.session.add(invoice)
        db.session.commit()
        InvoiceService.student_service.update_outstanding_balance(invoice.studentId)
        return invoice

    @staticmethod
    def get_invoice(reference):
        """
        Gets an invoice from a specified reference.

        Parameters:
        a (String): Reference of invoice to get.

        Return:
        An invoice object.
        """
        # Get an invoice from a reference
        invoice = Invoice.query.filter_by(reference=reference).first()
        return invoice

    @staticmethod
    def exists_invoice(reference):
        """
        Checks that an invoice of a given reference exists.

        Parameters:
        a (String): Reference of invoice to check.

        Return:
        Boolean true or false.
        """
        invoice = Invoice.query.filter_by(reference=reference).first()
        return invoice is not None

    @staticmethod
    def pay_invoice(reference):
        """
        Pays an outstanding invoice, setting status to paid.

        Parameters:
        a (String): Reference of invoice to pay.
        """
        # Pay an invoice from a reference
        invoice = InvoiceService.get_invoice(reference)
        invoice.status = "PAID"
        db.session.commit()
        InvoiceService.student_service.update_outstanding_balance(invoice.studentId)
        # Updates the outstanding balance of a student, in case this was their only outstanding invoice.
