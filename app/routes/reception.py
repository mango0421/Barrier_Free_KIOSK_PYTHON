# app/routes/reception.py - 접수 화면 입니다. /
import sys  # Added for logging
from flask import Blueprint, render_template, request, session, redirect, url_for

# Import service functions and SYMPTOMS list
from app.services.reception_service import (
    handle_scan_action,
    handle_manual_action,
    handle_choose_symptom_action,
    SYMPTOMS,  # SYMPTOMS is imported for use in the template
    update_reservation_status  # Added this import
)

reception_bp = Blueprint(
    "reception",
    __name__,
    url_prefix="/reception",
    template_folder="../../templates",
)

# Note: Added url_prefix="/reception" for consistency if other blueprints have it.
# Original did not have url_prefix for the blueprint itself, but relied on @reception_bp.route("/reception").
# This change makes routes like /reception/ instead of just /reception.
# If the old style /reception is required, the route below should be @reception_bp.route("/", methods=["GET", "POST"])
# and the blueprint registration should be Blueprint('reception', __name__, template_folder='../../templates')

# Definitions of BASE_DIR, RESV_CSV, SYMPTOMS, SYM_TO_DEPT, fake_scan_rrn,
# lookup_reservation, new_ticket are removed as they are now in the service.


@reception_bp.route("/", methods=["GET", "POST"])
# Changed to "/" assuming url_prefix handles /reception

def reception():
    _func_args = locals()
    _module_path = (
        sys.modules[__name__].__name__ if __name__ in sys.modules else __file__
    )
    print(f"ENTERING: {_module_path}.reception(args={{_func_args}})")

    if request.method == "POST":
        action = request.form.get("action")

        # 1) 주민등록증 인식 ---------------------------------------------------
        #    STEP 1‑A : 안내 화면만 먼저 보여 주기
        if action == "scan":
            # 사용자가 '주민등록증 인식' 버튼을 누른 직후.
            # 실제 스캔을 수행하기 전에 안내 메시지를 띄운다.
            return render_template("reception.html", step="scan_prompt")

        #    STEP 1‑B : '스캔 완료' 눌렀을 때 실제 스캔 로직 수행 (기존 코드 이동)
        elif action == "scan_execute":
            scan_result = handle_scan_action()  # Service returns dict with name, rrn, reservation_details
            session["patient_name"] = scan_result["name"]
            session["patient_rrn"] = scan_result["rrn"]

            if scan_result["reservation_details"]:
                update_reservation_status(scan_result["rrn"], "Registered")
                details = scan_result["reservation_details"]
                return render_template(
                    "reception.html",
                    step="reserved",
                    name=details.get("name"),
                    department=details.get("department"),
                    time=details.get("time"),
                    location=details.get("location"),
                    doctor=details.get("doctor"),
                )
            else:
                # If no reservation, they proceed to symptom choice. Status will be updated there.
                return render_template(
                    "reception.html",
                    step="symptom",
                    name=scan_result["name"],
                    rrn=scan_result["rrn"],
                    symptoms=SYMPTOMS,
                )

        # 2) 직접 입력 ---------------------------------------------------------
        elif action == "manual":
            name = request.form.get("name", "").strip()
            rrn = request.form.get("rrn", "").strip()

            if not name or not rrn:
                return render_template(
                    "reception.html",
                    step="input",
                    err="이름과 주민번호를 모두 입력하세요.",
                )  # symptoms=SYMPTOMS might be needed if form is re-shown

            session["patient_name"] = name
            session["patient_rrn"] = rrn

            reservation_details = handle_manual_action(name, rrn)  # Service returns dict or None

            if reservation_details:
                update_reservation_status(rrn, "Registered")
                # Note: reservation_details is already the correct dictionary here
                return render_template(
                    "reception.html",
                    step="reserved",
                    name=reservation_details.get("name"),
                    department=reservation_details.get("department"),
                    time=reservation_details.get("time"),
                    location=reservation_details.get("location"),
                    doctor=reservation_details.get("doctor"),
                )
            else:
                return render_template(
                    "reception.html",
                    step="symptom",
                    name=name,
                    rrn=rrn,
                    symptoms=SYMPTOMS,
                )

        # 3) 증상 선택 ---------------------------------------------------------
        elif action == "choose_symptom":
            symptom_key = request.form.get("symptom")

            # Session safety‑net: 사용자가 이전 단계를 건너뛰었을 가능성 방지
            if "patient_name" not in session or "patient_rrn" not in session:
                # Redirect to initial step if patient info is missing
                return redirect(url_for("reception.reception"))

            symptom_result = handle_choose_symptom_action(symptom_key)  # Returns dict with department, ticket

            session["department"] = symptom_result["department"]
            session["ticket"] = symptom_result["ticket"]

            patient_rrn_from_session = session.get("patient_rrn")  # Get rrn from session
            if patient_rrn_from_session:
                update_reservation_status(patient_rrn_from_session, "Registered")

            # Pass patient name to the ticket step as well, if needed by template
            patient_name = session.get("patient_name", "")

            return render_template(
                "reception.html",
                step="ticket",
                department=symptom_result["department"],
                ticket=symptom_result["ticket"],
                name=patient_name,
            )

    # GET → 접수 방법 선택 -----------------------------------------------------
    return render_template("reception.html", step="method")
