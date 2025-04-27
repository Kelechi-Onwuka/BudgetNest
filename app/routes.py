from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Transaction
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from flask import jsonify
main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    today = datetime.now().strftime("%A, %B, %d, %Y")
    # Get financial data
    total_income = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=current_user.id, type='income').scalar() or 0
    total_expenses = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=current_user.id, type='expense').scalar() or 0
    remaining = total_income - total_expenses
    return render_template('dashboard.html', today=today, total_income=total_income, total_expenses=total_expenses, remaining=remaining)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/signup')
def signup():
    return render_template('signup.html')


@main.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        
        print(f"Adding income: {amount}, {category}, {description}, user={current_user.id}")
        
        try:
            new_transaction = Transaction(
                type='income',
                amount=float(amount),  # Convert to float explicitly
                category=category,
                description=description,
                user_id=current_user.id
            )
            db.session.add(new_transaction)
            db.session.commit()
            print("Transaction added successfully!")
            print("All transactions now:", Transaction.query.all())

        except Exception as e:
            print(f"Error adding transaction: {e}")
            db.session.rollback()
        
        return redirect('/transactions')
    
    return render_template('income.html')

@main.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form.get('description', '')

        print(f"Adding expense: {amount}, {category}, {description}, user={current_user.id}")
        try:
            new_transaction = Transaction(
                type='expense',
                amount=float(amount),
                category=category,
                description=description,
                user_id=current_user.id
            )
            db.session.add(new_transaction)
            db.session.commit()
            print("Transaction added successfully!")
            print("All transactions now:", Transaction.query.all())
        except Exception as e:
            print(f"Error adding transaction: {e}")
            db.session.rollback()

        return redirect(url_for('main.view_transactions'))

    # GET just shows the form
    return render_template('expense.html')


@main.route('/transactions')
@login_required
def view_transactions():
    # Get filter parameters
    filter_type = request.args.get('type', '')
    filter_category = request.args.get('category', '')
    filter_start_date = request.args.get('start_date', '')
    filter_end_date = request.args.get('end_date', '')
    reset = request.args.get('reset', False)
    
    # Reset all filters if requested
    if reset:
        return redirect(url_for('main.view_transactions'))
    
    # Start with base query for current user
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if filter_type:
        query = query.filter_by(type=filter_type)
    
    if filter_category:
        query = query.filter_by(category=filter_category)
    
    if filter_start_date:
        start_date = datetime.strptime(filter_start_date, '%Y-%m-%d')
        query = query.filter(Transaction.date >= start_date)
    
    if filter_end_date:
        end_date = datetime.strptime(filter_end_date, '%Y-%m-%d')
        # Add one day to include the end date fully
        end_date = end_date + timedelta(days=1)
        query = query.filter(Transaction.date < end_date)
    
    # Execute the query
    transaction_list = query.all()
    
    # Get all categories for the filter dropdown
    categories = db.session.query(Transaction.category)\
                  .filter_by(user_id=current_user.id)\
                  .distinct()\
                  .order_by(Transaction.category)\
                  .all()
    categories = [category[0] for category in categories]  # Extract from result tuples
    
    # Calculate totals (based on filtered transactions)
    total_income = sum(t.amount for t in transaction_list if t.type == 'income')
    total_expenses = sum(t.amount for t in transaction_list if t.type == 'expense')
    remaining = total_income - total_expenses

    return render_template(
        'transactions.html',
        transactions=transaction_list,
        total_income=total_income,
        total_expenses=total_expenses,
        remaining=remaining,
        categories=categories,
        filter_type=filter_type,
        filter_category=filter_category,
        filter_start_date=filter_start_date,
        filter_end_date=filter_end_date
    )

@main.route('/api/totals')
@login_required
def api_totals():
    inc = db.session.query(func.sum(Transaction.amount))\
            .filter_by(user_id=current_user.id, type='income')\
            .scalar() or 0
    exp = db.session.query(func.sum(Transaction.amount))\
            .filter_by(user_id=current_user.id, type='expense')\
            .scalar() or 0
    return jsonify({
        'total_income': float(inc),
        'total_expenses': float(exp),
        'remaining': float(inc - exp)
    })

@main.route('/api/transactions')
@login_required
def api_transactions():
    # Get filter parameters from request
    filter_type = request.args.get('type', '')
    filter_category = request.args.get('category', '')
    filter_start_date = request.args.get('start_date', '')
    filter_end_date = request.args.get('end_date', '')
    
    # Start with base query for current user
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if filter_type:
        query = query.filter_by(type=filter_type)
    
    if filter_category:
        query = query.filter_by(category=filter_category)
    
    if filter_start_date:
        start_date = datetime.strptime(filter_start_date, '%Y-%m-%d')
        query = query.filter(Transaction.date >= start_date)
    
    if filter_end_date:
        end_date = datetime.strptime(filter_end_date, '%Y-%m-%d')
        # Add one day to include the end date fully
        end_date = end_date + timedelta(days=1)
        query = query.filter(Transaction.date < end_date)
    
    # Execute the query
    txs = query.all()
    
    return jsonify([
        {
          'id': t.id,
          'type': t.type,
          'amount': t.amount,
          'category': t.category,
          'description': t.description,
          'date': t.date.isoformat()
        } for t in txs
    ])