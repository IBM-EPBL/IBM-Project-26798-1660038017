from flask import Blueprint, current_app, flash, g, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import ibm_db
import ibm_db_dbi
import random
import os
from expense_tracker.auth import login_required
from expense_tracker.db import get_db
from expense_tracker.storage import multi_part_upload, get_signed_url
from expense_tracker.expense import get_current_month_expense
from expense_tracker.mailjet import send_email_alert
from datetime import datetime

bp = Blueprint('transaction', __name__, url_prefix='/transaction')


@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = g.user["ID"]
    query = f"SELECT transaction.amount, transaction.description, transaction.category, transaction.date, transaction.receipt FROM transaction INNER JOIN user ON transaction.user_id=user.id where user.id={user_id} ORDER BY transaction.id DESC"
    conn = ibm_db_dbi.Connection(db)
    curr = conn.cursor()
    curr.execute(query)
    transactions = curr.fetchall()
    return render_template('transaction/index.html', transactions=transactions)


@bp.route('/receipt/<receipt>')
def get_receipt(receipt):
    db = get_db()
    user_id = g.user["ID"]
    query = "SELECT * FROM transaction WHERE user_id=? AND receipt=?"
    stmt = ibm_db.prepare(db, query)
    ibm_db.bind_param(stmt, 1, user_id)
    ibm_db.bind_param(stmt, 2, receipt)
    try:
        ibm_db.execute(stmt)
    except:
        flash("Some error occurred")
    else:
        transaction = ibm_db.fetch_assoc(stmt)
        if not transaction:
            flash("No such receipt exists")
        else:
            return redirect(get_signed_url(receipt))
    return redirect(url_for('transaction.index'))


@bp.route('/all')
@login_required
def all():
    db = get_db()
    user_id = g.user["ID"]
    month = datetime.today().month
    year = datetime.today().year
    query = f"SELECT transaction.amount, transaction.description, transaction.category FROM transaction INNER JOIN user ON transaction.user_id=user.id WHERE MONTH(transaction.date)={month} AND YEAR(transaction.date)={year} AND user.id={user_id}"
    conn = ibm_db_dbi.Connection(db)
    curr = conn.cursor()
    curr.execute(query)
    transactions = curr.fetchall()
    return transactions


@bp.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        db = get_db()
        user_id = g.user["ID"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]
        date = request.form["date"]
        file = request.files['receipt']
        uuid = 'none'
        if not file.filename == '' and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uuid = multi_part_upload(file_path)
        current_expense = get_current_month_expense()
        insert = "INSERT INTO transaction (user_id, category, amount, description, date, receipt) VALUES (?, ?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare(db, insert)
        ibm_db.bind_param(stmt, 1, user_id)
        ibm_db.bind_param(stmt, 2, category)
        ibm_db.bind_param(stmt, 3, amount)
        ibm_db.bind_param(stmt, 4, description)
        ibm_db.bind_param(stmt, 5, date)
        ibm_db.bind_param(stmt, 6, uuid)
        error = None
        try:
            ibm_db.execute(stmt)
        except:
            error = "Error occurred while adding transaction"
        else:
            if current_expense < int(g.user["LIMIT"]) and current_expense + int(amount) > int(g.user["LIMIT"]):
                flash('Alert expense exceeds set limit')
                send_email_alert()
            return redirect(url_for('transaction.index'))
        flash(error)
    return render_template('transaction/add.html')


@bp.route('/limit', methods=["GET", "POST"])
@login_required
def limit():
    if request.method == "POST":
        db = get_db()
        id = g.user["ID"]
        limit = request.form["limit"]
        insert = f"UPDATE USER SET limit=? WHERE ID={id}"
        stmt = ibm_db.prepare(db, insert)
        ibm_db.bind_param(stmt, 1, limit)
        error = None
        try:
            ibm_db.execute(stmt)
        except:
            error = "Error occurred while setting limit"
        else:
            flash("Limit updated successfully")
            return redirect(url_for('dashboard.index'))
        flash(error)

    return render_template('transaction/limit.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']
