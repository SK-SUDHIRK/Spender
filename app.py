import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email, create_user

app = Flask(__name__)
# TODO: replace with os.environ value before production
app.secret_key = 'dev-spendly-secret-key-change-in-prod'

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('csrf_token') != session.get('csrf_token'):
            abort(400)

        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not all([name, email, password, confirm]):
            flash('All fields are required.')
            return render_template('register.html', csrf_token=session['csrf_token'])

        if password != confirm:
            flash('Passwords do not match.')
            return render_template('register.html', csrf_token=session['csrf_token'])

        if get_user_by_email(email):
            flash('An account with that email already exists.')
            return render_template('register.html', csrf_token=session['csrf_token'])

        create_user(name, email, generate_password_hash(password))
        return redirect(url_for('login'))

    csrf_token = secrets.token_hex(16)
    session['csrf_token'] = csrf_token
    return render_template('register.html', csrf_token=csrf_token)


@app.route("/login")
def login():
    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
