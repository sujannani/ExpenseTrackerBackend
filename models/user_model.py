from app import mongo
class user_model:
    def user_signup_model(self,user_data):
        try:
            existing_user = mongo.db.users.find_one({'email': user_data['email']})
            if existing_user:
                return {'message': 'Email already exists'}
            user=mongo.db.users.insert_one(user_data)
            return {'id':str(user.inserted_id),'message':'ok'}
        except Exception as e:
            return {'message':f"something went wrong{e}"}
    
    def user_login_model(self,user_data):
        print(user_data)
        try:
            user = mongo.db.users.find_one({'email': user_data['email'],'password':user_data['password']})
            if user:
                return {"message":"ok","user":{
                    'id':str(user['_id']),
                    'name':user['name'],
                    'email':user['email'],
                    'totalAmount':user['totalAmount']
                }}
            return {"message":"not ok","user":{}}
        except Exception as e:
            return {'message':f'{e}','user':{}}
    