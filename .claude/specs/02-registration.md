# Spec: Registration

## Overview
Implement the user registration flow so new visitors can create a Spendly account. This step wires up the `POST /register` route, validates the submitted form, hashes the password, inserts the new user into the database, and redirects to the login page on success. It also adds the two DB helper functions (`create_user`, `get_user_by_email`) that authentication steps will reuse.

## Depends on
- Step 1 — Database Setup (`users` table and `get_db()` must exist)

## Routes
- `GET /register` — render registration form — public (already exists, no change needed)
- `POST /register` — validate form, create user, redirect to `/login` — public

## Database changes
No new tables or columns. Two new helper functions must be added to `database/db.py`:

- `get_user_by_email(email)` — returns a `Row` or `None`
- `create_user(name, email, password_hash)` — inserts a row and returns the new `id`

## Templates
**Modify:** `templates/register.html`
- Add `<form method="POST" action="{{ url_for('register') }}">` wrapping all inputs
- Fields: `name` (text), `email` (email), `password` (password), `confirm_password` (password)
- Display flashed error messages above the form
- Include CSRF-safe hidden input (use Flask's built-in `secret_key` + `session`; no extra package)
- On success the page redirects away, so no success state needed in this template

## Files to change
- `app.py` — add `request`, `redirect`, `url_for`, `flash`, `session` to Flask imports; add `app.secret_key`; implement `POST /register` route; import new DB helpers
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — add form markup and flash message display

## Files to create
None

## New dependencies
No new pip packages. Uses:
- `werkzeug.security.generate_password_hash` (already installed)
- `flask.flash`, `flask.session`, `flask.request`, `flask.redirect`, `flask.url_for` (all in Flask)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before insert
- `app.secret_key` must be set (use a hard-coded dev string for now — flag that it must be an env var in production)
- Use `flash()` for user-facing error messages; render them in the template with `get_flashed_messages()`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validation order: (1) all fields present, (2) passwords match, (3) email not already registered
- On any validation failure: `flash()` the error and re-render `register.html` (do not redirect)
- On success: redirect to `url_for('login')` — do not auto-login the user in this step

## Definition of done
- [ ] Submitting the form with all valid fields creates a new row in `users` with a hashed password
- [ ] Submitting with a missing field shows an error message on the page without a redirect
- [ ] Submitting with mismatched passwords shows an error message on the page
- [ ] Submitting with an already-registered email shows an error message on the page
- [ ] Successful registration redirects to `/login`
- [ ] The demo user's email (`demo@spendly.com`) cannot be re-registered (duplicate email blocked)
- [ ] No plain-text password is stored in the database
- [ ] App starts without errors after changes
