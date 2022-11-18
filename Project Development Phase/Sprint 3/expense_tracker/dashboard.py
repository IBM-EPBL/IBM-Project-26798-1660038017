from flask import Blueprint, render_template, g
import ibm_db
import ibm_db_dbi
from datetime import datetime
from expense_tracker.auth import login_required
from expense_tracker.db import get_db
from expense_tracker.expense import get_current_month_expense

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def index():
    current_month_expense = get_current_month_expense()
    return render_template('dashboard/index.html', current_month_expense=current_month_expense)
