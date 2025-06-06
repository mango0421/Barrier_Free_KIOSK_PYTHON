from flask import Blueprint, render_template, request, redirect, url_for

reception_bp = Blueprint('reception', __name__, template_folder='../../templates')

@reception_bp.route('/reception', methods=['GET', 'POST'])
def reception():
    if request.method == 'POST':
        name = request.form.get('name')
        has_reservation = request.form.get('has_reservation') == 'yes'
        if has_reservation:
            department = "내과"
            return render_template('reception.html', step='reserved', department=department)
        else:
            return render_template('reception.html', step='select_symptom')
    return render_template('reception.html', step='input')
