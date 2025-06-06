from flask import Blueprint, render_template, request, redirect, url_for

certificate_bp = Blueprint('certificate', __name__, template_folder='../../templates')

@certificate_bp.route('/certificate', methods=['GET', 'POST'])
def certificate():
    if request.method == 'POST':
        step = request.form.get('step')
        if step == 'choose':
            doc_type = request.form.get('doc_type')
            return render_template('certificate.html', step='auth', doc_type=doc_type)
        elif step == 'auth':
            return render_template('certificate.html', step='payment')
        elif step == 'payment':
            return render_template('certificate.html', step='complete')
    return render_template('certificate.html', step='choose')
