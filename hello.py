from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'Database', 'store.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)

class RawInventory(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Text)
    product_cat = db.Column(db.Text)
    product_subcat = db.Column(db.Text)
    stock = db.Column(db.Integer)
    mrp = db.Column(db.Float)
    cost_price = db.Column(db.Float)
    vendor_phn = db.Column(db.Text)

class Employee(db.Model):
    emp_id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    contact_num = db.Column(db.Text)
    address = db.Column(db.Text)
    aadhar_num = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    designation = db.Column(db.Text)

class Bill(db.Model):
    bill_no = db.Column(db.Text, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    customer_name = db.Column(db.Text, nullable=False)
    customer_no = db.Column(db.Text, nullable=False)
    bill_details = db.Column(db.Text)

@app.route('/')
def index():
    # Fetch data from the database
    raw_inventory = RawInventory.query.all()
    employees = Employee.query.all()

    # Calculate total inventory size and total employees
    total_inventory_size = len(raw_inventory)
    total_employees = len(employees)

    # Calculate total bills generated and total customers
    total_bills_generated = Bill.query.count()
    total_customers = db.session.query(db.func.count(db.func.distinct(Bill.customer_no))).scalar()

    # Calculate inventory and employee distributions (if needed)

    return render_template('index.html',
                           total_inventory_size=total_inventory_size, total_employees=total_employees,
                           total_bills_generated=total_bills_generated, total_customers=total_customers)

@app.route('/inventory_data')
def get_inventory_data():
    inventory_data = {
        'Dairy': RawInventory.query.filter_by(product_cat='Dairy').count(),
        'Stationary': RawInventory.query.filter_by(product_cat='Stationary').count(),
        'Grocery': RawInventory.query.filter_by(product_cat='Grocery').count()
    }
    return jsonify(inventory_data)

@app.route('/employee_data')
def get_employee_data():
    employee_data = {
        'Cashier': Employee.query.filter_by(designation='Cashier').count(),
        'Custodian': Employee.query.filter_by(designation='Custodian').count(),
        'Others': Employee.query.filter(Employee.designation.notin_(['Cashier', 'Custodian'])).count()
    }
    return jsonify(employee_data)

if __name__ == '__main__':
    app.run(debug=True)
