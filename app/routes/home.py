from flask import Blueprint, render_template, session, redirect, url_for, request, current_app as app
import json, os

home_bp = Blueprint('home', __name__, template_folder='../../templates')

# 영어 리소스를 로드하는 간단 함수
def load_locale():
    lang = session.get('lang', 'ko')  # 기본값은 'ko'
    if lang == 'en':
        with open(os.path.join(os.getcwd(), 'locale', 'en.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}  # 한국어는 템플릿에 직접 한글을 넣어두고, 영어 리소스만 분리

@home_bp.route('/')
@home_bp.route('/home')
def home():
    locale = load_locale()
    font_size = session.get('font_size', 'normal')  # 'normal', 'large', 'small'
    return render_template('home.html', locale=locale, font_size=font_size)

@home_bp.route('/set-font/<size>')
def set_font(size):
    if size in ['small', 'normal', 'large']:
        session['font_size'] = size
    return redirect(url_for('home.home'))

@home_bp.route('/switch-language')
def switch_language():
    session['lang'] = 'en' if session.get('lang', 'ko') == 'ko' else 'ko'
    return redirect(url_for('home.home'))

# TTS용 아주 간단한 예시 (텍스트를 mp3로 변환해 반환)
@home_bp.route('/tts')
def tts():
    text = request.args.get('text', '')
    if not text:
        return '', 204
    from gtts import gTTS
    import io
    audio = io.BytesIO()
    tts = gTTS(text=text, lang='en' if session.get('lang') == 'en' else 'ko')
    tts.write_to_fp(audio)
    audio.seek(0)
    return app.response_class(audio, mimetype='audio/mp3')

# 비상 버튼 클릭 시(간단히 알림만)
@home_bp.route('/emergency')
def emergency():
    return "관리자에게 비상 알림을 보냈습니다.", 200
