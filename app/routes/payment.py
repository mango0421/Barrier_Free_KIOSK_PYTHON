"""
진료비 수납 (Blueprint)
    GET  /payment/  → 결제 폼
    POST /payment/  → 결제 완료 화면
"""
import uuid
from flask import Blueprint, render_template, request

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")
payments: list[dict] = []  # 메모리 결제 내역


@payment_bp.route("/", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        amount = float(request.form["amount"])
        method = request.form["method"]                 # cash | card | qr

        pay_id = uuid.uuid4().hex[:8].upper()
        payments.append(
            {"id": pay_id, "patient": patient_id, "amount": amount, "method": method}
        )

        return render_template(
            "payment.html",
            step="done",
            pay_id=pay_id,
            amount=amount,
            method=method,
        )

    # GET
    return render_template("payment.html", step="form")
