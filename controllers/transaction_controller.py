from flask import request # type: ignore
from app import app
from models.transaction_model import transaction_model

obj=transaction_model()

@app.route('/transactions/add_transaction',methods=["POST"])
def add_transaction_controller():
    return obj.add_transaction_model(request.get_json())

@app.route('/transactions/get_monthly_transactions',methods=["POST"])
def get_monthly_transactions_controller():
    return obj.get_monthly_transactions_model(request.get_json())

@app.route('/transactions/get_category_monthly_transactions',methods=['POST'])
def get_category_monthly_transactions_controller():
    return obj.get_category_monthly_transactions_model(request.get_json())

@app.route('/transactions/get_recent_transactions',methods=["POST"])
def get_recent_transactions_controller():
    return obj.get_recent_transactions_model(request.get_json())

@app.route('/transactions/edit_transaction',methods=['POST'])
def edit_transaction_controller():
    return obj.edit_transaction_model(request.get_json())

@app.route('/transactions/delete_transaction',methods=["POST"])
def delete_transaction_controller():
    return obj.delete_transaction_model(request.get_json())