import ibm_db
from flask import g
from datetime import datetime
from expense_tracker.db import get_db


def get_current_month_expense():
    id = g.user['ID']
    db = get_db()
    month = datetime.today().month
    year = datetime.today().year
    query = f'SELECT SUM(transaction.amount) FROM transaction INNER JOIN user on transaction.user_id=user.id WHERE MONTH(transaction.date)={month} and YEAR(transaction.date)={year} and user.id={id}'
    stmt = ibm_db.prepare(db, query)
    ibm_db.execute(stmt)
    result = ibm_db.fetch_assoc(stmt)['1']
    return 0 if result is None else int(result)
