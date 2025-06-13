# app/routes/reception.py - 접수 화면 입니다. /
import sys  
from flask import Blueprint, render_template, request, session, redirect, url_for

# 서비스 함수들과 증상 리스트를 불러 옵니다.
from app.services.reception_service import (
    handle_scan_action,
    handle_manual_action,
    handle_choose_symptom_action,
    SYMPTOMS,  #증상들은 템플릿에 올라온 내용을 바탕으로 진행합니다
    update_reservation_status
)

reception_bp = Blueprint(
    "reception",
    __name__,
    url_prefix="/reception",
    template_folder="../../templates",
)

@reception_bp.route("/", methods=["GET", "POST"])
# 파이썬 flask 프레임 워크 쓰기 - 서버 받아오는 등의 역할


#reception 접수 할때 사용하는 함수
def reception():
    _func_args = locals()
    _module_path = (
        sys.modules[__name__].__name__ if __name__ in sys.modules else __file__
    )
    print(f"ENTERING: {_module_path}.reception(args={{_func_args}})")

    if request.method == "POST":
        action = request.form.get("action")

        # 1) 주민등록증 인식 ---------------------------------------------------
        #    1)-1 : 안내 화면만 먼저 보여 주기
        if action == "scan":
            # 사용자가 '주민등록증 인식' 버튼을 누른 직후.
            # 실제 스캔을 수행하기 전에 안내 메시지를 띄운다.
            return render_template("reception.html", step="scan_prompt")

        #    1)-2 : '스캔 완료' 눌렀을 때 실제 스캔 로직 수행 (기존 코드 이동)
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
                # 예약 내역이 없다면 증상을 선택하고 증상에 맞는 진료과를 추천해 줍니다.
                return render_template(
                    "reception.html",
                    step="symptom",
                    name=scan_result["name"],
                    rrn=scan_result["rrn"],
                    symptoms=SYMPTOMS,
                )

        #
        elif action == "manual":
            name = request.form.get("name", "").strip()
            rrn = request.form.get("rrn", "").strip()

            if not name or not rrn:
                return render_template(
                    "reception.html",
                    step="input",
                    err="이름과 주민번호를 모두 입력하세요.",
                )  

            session["patient_name"] = name
            session["patient_rrn"] = rrn

            reservation_details = handle_manual_action(name, rrn)  

            if reservation_details:
                update_reservation_status(rrn, "Registered")
                
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

            
            if "patient_name" not in session or "patient_rrn" not in session:
                
                return redirect(url_for("reception.reception"))

            symptom_result = handle_choose_symptom_action(symptom_key)  

            session["department"] = symptom_result["department"]
            session["ticket"] = symptom_result["ticket"]

            patient_rrn_from_session = session.get("patient_rrn")  
            if patient_rrn_from_session:
                update_reservation_status(patient_rrn_from_session, "Registered")

            
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
