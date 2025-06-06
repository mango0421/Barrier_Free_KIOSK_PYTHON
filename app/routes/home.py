from flask import Blueprint, render_template, session, redirect, url_for, request, current_app as app
import json, os

home_bp = Blueprint('home', __name__, template_folder='../../templates')

# ---------- locale util ----------
def load_locale():
    lang = session.get('lang', 'ko')
    if lang == 'en':
        with open(os.path.join(os.getcwd(), 'locale', 'en.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}          # 한국어는 바로 템플릿에 기재

# ---------- routes ----------
@home_bp.route('/')
@home_bp.route('/home')
def home():
    locale     = load_locale()
    font_size  = session.get('font_size', 'normal')
    audio_url  = url_for('static', filename='audio/audio_1_kor.mp3')  # ★ 추가
    return render_template(
        'home.html',
        locale=locale,
        font_size=font_size,
        audio_url=audio_url        # ★ 템플릿으로 전달
    )

@home_bp.route('/set-font/<size>')
def set_font(size):
    if size in ['small', 'normal', 'large']:
        session['font_size'] = size
    return redirect(url_for('home.home'))

@home_bp.route('/switch-language')
def switch_language():
    session['lang'] = 'en' if session.get('lang', 'ko') == 'ko' else 'ko'
    return redirect(url_for('home.home'))

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

@home_bp.route('/emergency')
def emergency():
    return "관리자에게 비상 알림을 보냈습니다.", 200
