from . import edit
from flask_login import login_required, current_user
from flask import render_template, url_for, redirect, abort, current_app, flash, request, jsonify
import requests
from .forms import DeleteUserWithFolderForm, DeleteUserWithoutFolderForm, AddUserToGroupForm

AGENT_URL = "http://agent-container:5005"  # Adres agenta

# Funkcja do pobierania tokenu
def get_token():
    """Uzyskuje token JWT z agenta."""
    login_url = f"{AGENT_URL}/login"
    credentials = {"username": "admin", "password": "admin123"}  # Dane logowania agenta
    try:
        response = requests.post(login_url, json=credentials)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            flash("Nie udało się zalogować do agenta.", "danger")
    except Exception as e:
        flash(f"Błąd podczas logowania do agenta: {e}", "danger")
    return None

# Funkcja do komunikacji z agentem
def send_request_to_agent(endpoint, payload):
    """Wysyła żądanie do agenta z tokenem."""
    token = get_token()
    if not token:
        return None  # Nie można wysłać żądania bez tokenu

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{AGENT_URL}/{endpoint}", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Błąd komunikacji z agentem: {response.status_code}", "danger")
    except Exception as e:
        flash(f"Błąd podczas komunikacji z agentem: {e}", "danger")
    return None

@edit.route('/user_edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    try:
        response = send_request_to_agent("available_users", {})
        if not response or response.get("status") != "success":
            flash("Nie udało się pobrać danych użytkowników i grup.", "danger")
            return redirect(url_for("main.index"))

        users = [{"name": user} for user in response.get("users", [])]
        groups = response.get("groups", [])

        # Tworzenie formularzy dla każdego użytkownika
        user_forms = []
        for user in users:
            delete_with_folder_form = DeleteUserWithFolderForm(username=user['name'])
            delete_without_folder_form = DeleteUserWithoutFolderForm(username=user['name'])
            add_to_group_form = AddUserToGroupForm(username=user['name'])
            add_to_group_form.group.choices = [(group, group) for group in groups]  # Ustaw dostępne grupy
            user_forms.append({
                "user": user,
                "delete_with_folder_form": delete_with_folder_form,
                "delete_without_folder_form": delete_without_folder_form,
                "add_to_group_form": add_to_group_form
            })

        return render_template('edit/user_edit.html', user_forms=user_forms)
    except Exception as e:
        if current_app.debug:
            print(e)
        abort(404)


@edit.route('/delete_user_with_folder', methods=['POST'])
@login_required
def delete_user_with_folder():
    user_form = DeleteUserWithFolderForm()
    if user_form.validate_on_submit():
        username = user_form.username.data

        if not username:
            flash('Nie podano nazwy użytkownika', 'danger')
            return redirect(url_for('edit.user_edit'))

        payload = {"username": username}
        response = send_request_to_agent("remove_with_folder", payload)

        if response and response.get("status") == "success":
            flash(f"Użytkownik {username} został usunięty z folderem: {response.get('message')}", 'success')
        else:
            flash(f"Nie udało się usunąć użytkownika: {response.get('message')}", 'danger')
    else:
        flash('Nieprawidłowe dane w formularzu', 'danger')

    return redirect(url_for('edit.user_edit'))


@edit.route('/delete_user_without_folder', methods=['POST'])
@login_required
def delete_user_without_folder():
    user_form = DeleteUserWithoutFolderForm()
    if user_form.validate_on_submit():
        username = user_form.username.data

        if not username:
            flash('Nie podano nazwy użytkownika', 'danger')
            return redirect(url_for('edit.user_edit'))

        payload = {"username": username}
        response = send_request_to_agent("remove_without_folder", payload)

        if response and response.get("status") == "success":
            flash(f"Użytkownik {username} został usunięty bez folderu: {response.get('message')}", 'success')
        else:
            flash(f"Nie udało się usunąć użytkownika: {response.get('message')}", 'danger')
    else:
        flash('Nieprawidłowe dane w formularzu', 'danger')

    return redirect(url_for('edit.user_edit'))


@edit.route('/add_user_to_group', methods=['POST'])
@login_required
def add_user_to_group():
    form = AddUserToGroupForm()
    print("My FOOOOOOOOORM IS ", form)

    if form.validate_on_submit():
        print("POWINNO BYYYYYYYYYYC")
        username = form.username.data
        print(username, 'USERNAMEEEEEEEEEEEEEEEEEEEEEEEEE')
        group = form.group.data

        if not username or not group:
            flash('Nie podano nazwy użytkownika lub grupy', 'danger')
            return redirect(url_for('edit.user_edit'))

        print(username, group, "MOJJJJJJEEEEEEEEEEEEEEE")
        payload = {"username": username, "group": group}
        response = send_request_to_agent("add_user_to_group", payload)

        if response and response.get("status") == "success":
            flash(f"Użytkownik {username} został dodany do grupy {group}.", 'success')
        else:
            flash(f"Nie udało się dodać użytkownika do grupy: {response.get('message')}", 'danger')
    else:
        flash('Nieprawidłowe dane w formularzu', 'danger')

    return redirect(url_for('edit.user_edit'))
