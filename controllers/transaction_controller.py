from flask import request # type: ignore
from app import app
from models.transaction_model import transaction_model

obj=transaction_model()

@app.route('/transactions/add_transaction',methods=["POST"])
def add_transaction_controller():
    return obj.add_transaction_model(request.form.to_dict())

@app.route('/transactions/get_monthly_transactions',methods=["POST"])
def get_monthly_transactions_controller():
    return obj.get_monthly_transactions_model(request.form.to_dict())

@app.route('/transactions/get_category_monthly_transactions',methods=['POST'])
def get_category_monthly_transactions_controller():
    return obj.get_category_monthly_transactions_model(request.form.to_dict())