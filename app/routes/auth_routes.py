# app/auth/routes.py
from flask import Blueprint, request, jsonify, render_template,session,redirect
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from app.models.user import User
from app.forms.auth_forms import RegisterForm
from app.forms.auth_forms import LoginForm
from app.forms.expense_form import ExpenseForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/")
def home():
    return render_template("index.html")

# ------------------------
# HTML Form Registration
@auth_bp.route('/register', methods=['GET'])
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)

# ------------------------
# API Registration (JSON/Form)
# ------------------------
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    try:
        # Try JSON first, fallback to form data
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        email = data.get('email')        # 🔥 added
        password = data.get('password')

        # Validate required fields
        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user and save
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Registered successfully"}), 201

    except Exception as e:
        # Detailed error only for development
        return jsonify({"error": f"Server error: {str(e)}"}), 500
# ------------------------
# Dashboard route
# ------------------------
@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    username = session.get('username', 'Guest')
    form = ExpenseForm()

    return render_template(
        'dashboard.html',
        form =form,
        username=username
    )


@auth_bp.route('/login', methods=['GET'])
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "All fields required"}), 400

    # 🔥 Check DB
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

    # 🔥 Session login
    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({"message": "Login successful"}), 200


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')