from flask import Flask, render_template
from sqlalchemy import func
from db import db
from forms import ExpenseForm, CategoryForm
from models import ExpenseModel, Category


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_data.db'
app.config['SECRET_KEY'] = 'bardzo_tajny_klucz'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


@app.route("/", methods=['GET', 'POST'])
def handle_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        name = form.name.data
        value = round(form.value.data, 2)
        category = form.category.data
        expense = ExpenseModel(name=name, value=value, category_id=category)
        db.session.add(expense)
        db.session.commit()

    return render_template('main.html', form=form)


@app.route("/category", methods=['GET', 'POST'])
def handle_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
    return render_template('category.html', form=form)


@app.route("/summary", methods=['GET'])
def get_summary():
    result_db = ExpenseModel.query.all()
    sum_all = round(sum(task.value for task in result_db), 2)

    category_expenses = db.session.query(
        Category.name,
        func.round(func.sum(ExpenseModel.value), 2),
        func.round(((func.sum(ExpenseModel.value)) / sum_all) * 100, 2)
    ).join(ExpenseModel).group_by(Category.name).all()

    return render_template("summary.html", sum_all=sum_all, category_expenses=category_expenses)


@app.route("/expenses", methods=['GET'])
def get_expenses():
    expenses_with_categories = db.session.query(ExpenseModel, Category).join(
        Category,
        ExpenseModel.category_id == Category.id
    ).all()
    return render_template("expenses.html", expenses_with_categories=expenses_with_categories)

if __name__ == "__main__":
    app.run(debug=True)