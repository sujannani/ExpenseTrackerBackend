from app import app
from flask import request # type: ignore
from models.user_model import user_model

obj=user_model()

@app.route('/users/signup',methods=["POST"])
def user_signup_controller():
    return obj.user_signup_model(request.form.to_dict())

@app.route('/users/login',methods=["POST"])
def user_login_controller():
    print(request.form.to_dict())
    return obj.user_login_model(request.form.to_dict())

