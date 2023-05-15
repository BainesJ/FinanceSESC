from flask import Blueprint, render_template, Flask, request, jsonify
from services import studentService

studentController = Blueprint("studentController", __name__)
service = studentService.StudentService


@studentController.route("/api/get-outstanding-invoices", methods=["POST"])
def get_outstanding_invoices():
    """
    POST endpoint, gets a list of all references for outstanding invoices for a given student ID.

    Parameters:
    a (String): The student ID to receive references for.

    Returns:
    A list of references for all associated invoices that are outstanding.
    """
    student_id = request.json["studentId"]
    print(student_id)
    answer = service.get_outstanding_references(student_id)
    print(answer)
    return jsonify(answer)
