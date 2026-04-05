# app/expenses/routes.py
from flask import Blueprint, request, jsonify, session
from app import db
from app.models.expenses import Expense
from functools import wraps
from datetime import datetime, timedelta

expenses_bp = Blueprint('expenses', __name__)

# ------------------------
# Login required decorator
# ------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated

# ------------------------
# Get all expenses
# ------------------------
@expenses_bp.route("/api/expenses", methods=["GET"])
@login_required
def get_expenses(user_id):
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify({
        "expenses": [
            {
                "id": e.id,
                "amount": e.amount,
                "category": e.category,
                "description": e.description,
                "date": e.date.strftime("%Y-%m-%d")
            } for e in expenses
        ],
        "total": sum(e.amount for e in expenses)
    })

# ------------------------
# Add expense
# ------------------------
@expenses_bp.route("/api/add-expense", methods=["POST"])
@login_required
def add_expense(user_id):
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        amount = data.get("amount")
        category = data.get("category")
        description = data.get("description", "")

        if not amount or not category:
            return jsonify({"error": "Amount & Category required"}), 400

        expense = Expense(
            user_id=user_id,
            amount=float(amount),
            category=category,
            description=description
        )
        db.session.add(expense)
        db.session.commit()

        return get_expenses()  # return updated list
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------
# Edit expense
# ------------------------
@expenses_bp.route("/api/edit-expense/<int:id>", methods=["PUT"])
@login_required
def edit_expense(id, user_id):
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        expense = Expense.query.filter_by(id=id, user_id=user_id).first()
        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        expense.amount = float(data.get("amount", expense.amount))
        expense.category = data.get("category", expense.category)
        expense.description = data.get("description", expense.description)
        db.session.commit()

        return get_expenses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------
# Delete expense
# ------------------------
@expenses_bp.route("/api/delete-expense/<int:id>", methods=["DELETE"])
@login_required
def delete_expense(id, user_id):
    try:
        expense = Expense.query.filter_by(id=id, user_id=user_id).first()
        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        db.session.delete(expense)
        db.session.commit()
        return get_expenses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@expenses_bp.route("/api/filter-expenses", methods=["GET"])
def filter_expenses():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    start = request.args.get("start", "")
    end = request.args.get("end", "")

    query = Expense.query.filter_by(user_id=user_id)

    try:
        # If only start is provided, set end = start
        if start and not end:
            end = start

        if start:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            query = query.filter(Expense.date >= start_date)
        if end:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            # Include the whole end day
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
            query = query.filter(Expense.date <= end_date)

        expenses = query.order_by(Expense.date.desc()).all()

        return jsonify({
            "expenses": [
                {
                    "id": e.id,
                    "amount": e.amount,
                    "category": e.category,
                    "description": e.description,
                    "date": e.date.strftime("%Y-%m-%d")
                } for e in expenses
            ],
            "total": sum(e.amount for e in expenses)
        })

    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400
# ------------------------
# Monthly report
# ------------------------
@expenses_bp.route("/api/monthly-report", methods=["GET"])
@login_required
def monthly_report(user_id):
    try:
        month = request.args.get("month")  # format yyyy-mm
        if not month:
            return jsonify({"error": "Month parameter required"}), 400

        year, month_num = map(int, month.split("-"))

        expenses = Expense.query.filter(
            Expense.user_id == user_id,
            db.extract('year', Expense.date) == year,
            db.extract('month', Expense.date) == month_num
        ).all()

        report = {}
        for e in expenses:
            report[e.category] = report.get(e.category, 0) + e.amount

        return jsonify({
            "report": report,
            "total": sum(report.values())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500