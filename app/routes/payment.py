from flask import Blueprint, render_template, request, redirect, url_for

payment_bp = Blueprint('payment', __name__, template_folder='../../templates')

@payment_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        step = request.form.get('step')
        if step == 'input':
            return render_template('payment.html', step='pay')
        elif step == 'pay':
            return render_template('payment.html', step='complete')
    return render_template('payment.html', step='input')
