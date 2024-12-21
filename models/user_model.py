from bson import ObjectId
from app import mongo,bcrypt
from datetime import datetime, timezone

class user_model:
    def user_signup_model(self,user_data):
        try:
            existing_user = mongo.db.users.find_one({'email': user_data['email']})
            if existing_user:
                return {'message': 'Email already exists'}
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user_data['password'] = hashed_password
            user_data['totalAmount']=0
            user_data['createdAt']=datetime.now(timezone.utc).isoformat()
            user=mongo.db.users.insert_one(user_data)
            return {'id':str(user.inserted_id),'message':'success'}
        except Exception as e:
            return {'message':f"something went wrong{e}"}
    
    def user_login_model(self,user_data):
        try:
            user = mongo.db.users.find_one({'email': user_data['email']})
            if user:
                if bcrypt.check_password_hash(user['password'], user_data['password']):
                    return {"message":"success","user":{
                        'id':str(user['_id']),
                        'name':user['name'],
                        'email':user['email'],
                        'totalAmount':user['totalAmount']
                    }}
                return {"message": "Invalid credentials", "user": {}}
            return {"message":"User not found","user":{}}
        except Exception as e:
            return {'message':f'{e}','user':{}}
    
    