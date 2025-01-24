import requests

from .forms import AddUserForm, AddTeacherForm
from . import main
from flask import render_template, url_for, redirect, abort, current_app, flash, request
from flask_login import login_required, current_user



@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    try:
        if current_user.is_authenticated:
            return render_template('main/index.html')
        else:
            return redirect(url_for('auth.login'))
    except Exception as e:
        if current_app.debug:
            print(e)
        abort(404)

@main.route('/choose_option', methods=['GET', 'POST'])
@login_required
def choose_option():
    """
    This funciton returns view with 2 buttons option to choose. Add student or teacher. That's all
    """
    try:
        if current_user.is_authenticated:
            return render_template('main/choose_option.html')
        else:
            return redirect(url_for('auth.login'))
    except Exception as e:
        if current_app.debug:
            print(e)
        abort(404)


@main.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    try:
        form = AddUserForm()
        return render_template('main/add_user.html', form=form)

    except Exception as e:
        if current_app.debug:
            print(e)
        abort(404)


@main.route('/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    try:
        form = AddTeacherForm()
        return render_template('main/add_teacher.html', form=form)

    except Exception as e:
        if current_app.debug:
            print(e)
        abort(404)


@main.route('/copy_data', methods=['GET', 'POST'])
@login_required
def copy_data():
    try:
        user_form = AddUserForm()
        username = user_form.user_login.data

        teacher_form = AddTeacherForm()
        teacher_name = teacher_form.teacher_login.data


        if username is None and teacher_name is None:
            abort(404)

        # Ustal, który login przesłać
        data_to_send = username if username else teacher_name

        # Przygotowanie danych do wysłania do agenta
        if data_to_send == username:
            data_to_copy = send_message(data_to_send)
            if data_to_copy:
                return render_template('main/copy_data.html',
                                       data_to_copy=data_to_copy,
                                       flash=flash,
                                       last_action="add_user")
            else:
                return redirect(url_for('main.choose_option'))

        if data_to_send == teacher_name:
            data_to_copy = send_message(data_to_send, key="teacher_name")
            if data_to_copy:
                return render_template('main/copy_data.html',
                                       data_to_copy=data_to_copy,
                                       flash=flash,
                                       last_action="add_teacher")
            else:
                return redirect(url_for('main.choose_option'))

        return redirect(url_for('main.copy_data'))

    except Exception as e:
        if current_app.debug:
            print(f"Błąd: {e}")
        abort(404)


def get_token():
    """
    Uzyskuje token JWT z agenta.
    """
    login_url = "http://agent-container:5005/login"  # Endpoint logowania w agencie
    credentials = {
        "username": "admin",  # Użytkownik agenta
        "password": "admin123"  # Hasło agenta
    }
    try:
        response = requests.post(login_url, json=credentials)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            flash("Nie udało się zalogować do agenta.", "danger")
            return False
    except Exception as e:
        flash(f"Błąd podczas logowania do agenta: {e}", "danger")
        return False


def send_message(data_to_send, key="username"):
    """
    Wysyła dane do agenta API i odbiera odpowiedź.
    """
    token = get_token()
    if not token:
        abort(400)

    payload = {key: data_to_send}
    headers = {"Authorization": f"Bearer {token}"}

    agent_endpoints = {
        "username": "http://agent-container:5005/add_user",
        "teacher_name": "http://agent-container:5005/add_admin"
    }

    agent_url = agent_endpoints.get(key)

    if not agent_url:
        abort(400)

    try:
        response = requests.post(agent_url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                data_to_copy = result.get("data_to_copy")
                flash(f'Użytkownik {data_to_send} został pomyślnie dodany!', 'success')
                return data_to_copy
            else:
                abort(500)
        else:
            abort(404)
    except Exception:
        abort(404)
