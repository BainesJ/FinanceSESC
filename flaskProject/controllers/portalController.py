from flask import Blueprint, render_template, Flask, request, jsonify
from services import invoiceService

portalController = Blueprint("portalController", __name__)
service = invoiceService.InvoiceService()


@portalController.get("/portal")
def portal_get():
    """
    GET endpoint for the portal of the finance service.

    Returns:
    A render template of the portal html page.
    """
    return render_template("portal.html")


@portalController.post("/portal")
def portal_post():
    """
    POST endpoint for the invoice checking page of the finance service.

    Returns:
    A render template of the portal html page if reference isn't found, or to an invoice's html page if it is found.
    """
    reference = request.form.get("reference")
    if service.exists_invoice(reference):
        return render_template("invoice.html", invoice=service.get_invoice(reference))
    else:
        return render_template("portal.html", message="Reference not found.")


@portalController.get("/invoice")
def invoice_get():
    """
    GET endpoint of an invoice page of the finance service.

    Returns:
    A render template of the invoice page of the specified reference.
    """
    reference = request.json["reference"]
    return render_template("invoice.html", invoice=service.get_invoice(reference))


@portalController.post("/invoice")
def invoice_post():
    """
    POST endpoint of an invoice page of the finance service.

    Returns:
    A render template of the invoice page of the specified reference, updating if the invoice has been paid.
    """
    reference = request.form.get("reference")
    service.pay_invoice(reference)
    return render_template("invoice.html", invoice=service.get_invoice(reference))
