"""
증명서 발급 (Blueprint)
    GET  /certificate/  → 입력 폼
    POST /certificate/  → 발급 완료 화면
"""
import uuid
from flask import Blueprint, render_template, request

certificate_bp = Blueprint("certificate", __name__, url_prefix="/certificate")

issued_certs: list[dict] = []  # 간단한 메모리 저장소


@certificate_bp.route("/", methods=["GET", "POST"])
def certificate():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        cert_type = request.form["cert_type"]           # diagnosis | visit | vaccination
        payment_method = request.form["payment_method"] # cash | card | qr

        cert_no = uuid.uuid4().hex[:8].upper()
        issued_certs.append(
            {"no": cert_no, "patient": patient_id, "type": cert_type}
        )

        return render_template(
            "certificate.html",
            step="done",
            cert_no=cert_no,
            cert_type=cert_type,
            payment_method=payment_method,
        )

    # GET
    return render_template("certificate.html", step="form")

