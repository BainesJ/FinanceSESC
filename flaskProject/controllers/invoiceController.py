from flask import Blueprint, render_template, Flask, request, jsonify
from services import invoiceService

invoiceController = Blueprint("invoiceController", __name__)
service = invoiceService.InvoiceService()


@invoiceController.route("/api/invoice/create_invoice", methods=["POST"])
def create_invoice():
    """
    POST API used to create invoices with the microservice.

    Parameters:
    a (Invoice): An invoice to instantiate in the database, allowing payment or cancellation.

    Returns:
    A serialized invoice object that has been created on the finance service.
    """
    invoice = request.json
    # Converting the request into an invoice, to read pertinent information from.
    result = service.create_invoice(invoice)
    serialized_invoice = {
        "reference": result.reference,
        "amount": result.amount,
        "dueDate": result.dueDate.isoformat(),
        "type": result.type,
        "status": result.status,
        "studentId": result.studentId,
    }
    return jsonify(serialized_invoice)