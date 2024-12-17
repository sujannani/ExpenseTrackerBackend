from app import app
from flask import request # type: ignore
from models.category_model import category_model

obj=category_model()

@app.route('/category/add_category',methods=["POST"])
def add_category_controller():
    return obj.add_category_model(request.form.to_dict())

@app.route('/category/<id>/get_categories')
def get_categories_model(id):
    return obj.get_categories_model(id)

@app.route('/category/edit_category',methods=["POST"])
def edit_category_controller():
    return obj.edit_category_model(request.form.to_dict())

@app.route('/category/delete_category',methods=["POST"])
def delete_category_controller():
    return obj.delete_category_model(request.form.to_dict())