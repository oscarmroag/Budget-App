from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Category, Paycheck

main_routes = Blueprint('main', __name__)  # <== This line defines the blueprint


@main_routes.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.categories'))

# Route to view all categories for a specific paycheck
@main_routes.route('/categories', methods=['GET'])
def categories():
    # Fetch categories for the most recent paycheck (or customize for your use case)
    paycheck = Paycheck.query.order_by(Paycheck.end_date.desc()).first()
    categories = Category.query.filter_by(paycheck_id=paycheck.id).all()
    return render_template('categories.html', categories=categories)

# Route to add a new category
@main_routes.route('/categories', methods=['POST'])
def add_category():
    name = request.form.get('name')
    budget = request.form.get('budget', type=float)
    paycheck = Paycheck.query.order_by(Paycheck.end_date.desc()).first()

    new_category = Category(name=name, budget=budget, paycheck_id=paycheck.id)
    db.session.add(new_category)
    db.session.commit()

    return redirect(url_for('main.categories'))

# Route to update a category's budget
@main_routes.route('/categories/<int:id>', methods=['POST'])
def update_category(id):
    category = Category.query.get_or_404(id)
    category.budget = request.form.get('budget', type=float)
    db.session.commit()
    return redirect(url_for('main.categories'))

# Route to delete a category
@main_routes.route('/categories/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('main.categories'))
