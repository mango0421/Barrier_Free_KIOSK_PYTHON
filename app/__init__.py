# app/__init__.py

from flask import Flask

# Blueprint를 등록하기 위해 import
from app.routes.home        import home_bp
from app.routes.reception   import reception_bp
from app.routes.certificate import certificate_bp
from app.routes.payment     import payment_bp

def create_app():
    # Flask 인스턴스 생성
    #  - static_folder: app/static/ 내부에서 정적파일을 찾도록 설정
    #  - template_folder: app/templates/ 내부에서 템플릿을 찾도록 설정
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    # (선택) 세션 암호키 설정 (환경변수로 관리하는 것이 권장됩니다)
    app.secret_key = 'replace-with-your-secret'

    # ── 등록된 Blueprint들을 붙여 줍니다 ──────────────────────────────────
    # home_bp       : "/" 혹은 필요에 따라 url_prefix="/" 등으로 라우팅
    # reception_bp  : "/reception" 등의 URL에 대응
    # certificate_bp: "/certificate" 등의 URL에 대응
    # payment_bp    : "/payment" 등의 URL에 대응

    app.register_blueprint(home_bp)
    app.register_blueprint(reception_bp)
    app.register_blueprint(certificate_bp)
    app.register_blueprint(payment_bp)

    return app
