from bson import ObjectId
from datetime import datetime,timedelta,timezone
import dateutil.parser
from app import mongo
class transaction_model:
    def add_transaction_model(self,transaction_data):
        try:
            transaction_data['date'] = datetime.now(timezone.utc)
            transaction_data['amount'] = float(transaction_data['amount'])
            transaction=mongo.db.transactions.insert_one(transaction_data)
            update_value = transaction_data['amount'] if transaction_data['type'] == "credit" else -transaction_data['amount']
            update_result = mongo.db.users.update_one(
                {'_id': ObjectId(transaction_data['user_id'])},
                {'$inc': {'totalAmount': update_value}}
            )
            if update_result.matched_count==0:
                return {'message':"can't update total amount"}
            return {"message":'success','transaction_id':str(transaction.inserted_id)}
        except Exception as e:
            print(f"error is {e}")
            return {'message':f'wrong is e'}
    
    def get_monthly_transactions_model(self,input_data):
        try:
            start_date =dateutil.parser.parse(input_data['start_date'])
            end_date = dateutil.parser.parse(input_data['end_date'])
            user = mongo.db.users.find_one({'_id': ObjectId(input_data['user_id'])})
            created_at = user.get('createdAt')
            created_at=created_at.replace(tzinfo=timezone.utc)
            if end_date < created_at:
                return {'message': 'No more transactions available'}

            transactions = list(mongo.db.transactions.find({
                'user_id': input_data['user_id'],
                'date': {
                    '$gte': start_date,
                    '$lt': end_date
                }
            }))
            timezone_offset = start_date.utcoffset()
            offset_hours = timezone_offset.seconds // 3600
            offset_minutes = (timezone_offset.seconds // 60) % 60
            for transaction in transactions:
                transaction['_id']=str(transaction['_id'])
                transaction['date'] = (transaction['date'] + timedelta(hours=offset_hours, minutes=offset_minutes)).isoformat()
            return {"monthly_transactions":{'transactions':transactions,'date':input_data['start_date']},'message':'success'}
        except Exception as e:
            return {'message':str(e)}
    
    def get_category_monthly_transactions_model(self,input_data):
        try:
            start_date = dateutil.parser.parse(input_data['start_date'])
            end_date = dateutil.parser.parse(input_data['end_date'])
            user = mongo.db.users.find_one({'_id': ObjectId(input_data['user_id'])})
            created_at = user.get('createdAt')
            created_at=created_at.replace(tzinfo=timezone.utc)
            if end_date < created_at:
                return {'message': 'No more transactions available'}
            transactions = list(mongo.db.transactions.aggregate([
                {
                    '$match': {
                        'user_id': input_data['user_id'],
                        'date': {'$gte': start_date, '$lt': end_date}
                    }
                },
                {
                    '$group': {
                        '_id': '$category_id',
                        'total_cost': {
                            '$sum': {
                                '$cond': [
                                    {'$eq': ['$type', 'credit']},
                                    '$amount',                    
                                    {'$multiply': ['$amount', -1]} 
                                ]
                            }
                        },
                        'count': {'$sum': 1}
                    }
                }
            ]))            
            return {'message':"success",'category_monthly_transactions':{"category_transactions":transactions,'date':input_data['start_date']}}
        except Exception as e:
            return {'message':str(e)}
    
    def get_recent_transactions_model(self,user_data):
        try:
            recent_transactions = list(mongo.db.transactions.find({
                "user_id": user_data['user_id']
            }).sort("date", -1).limit(5))
            user = mongo.db.users.find_one({'_id': ObjectId(user_data['user_id'])})
            total_amount = user.get('totalAmount')
            start_date_parsed = dateutil.parser.parse(user_data['date'])
            timezone_offset = start_date_parsed.utcoffset()
            offset_hours = timezone_offset.seconds // 3600
            offset_minutes = (timezone_offset.seconds // 60) % 60
            for transaction in recent_transactions:
                transaction["_id"] = str(transaction["_id"])
                transaction['date'] = (transaction['date'] + timedelta(hours=offset_hours, minutes=offset_minutes)).isoformat()
            return {"message":"success",'transactions':recent_transactions,'total_amount':total_amount}
        except Exception as e:
            return {'message':str(e)}
        
    def delete_transaction_model(self,transaction_data):
        try:
            transaction = mongo.db.transactions.find_one({'_id': ObjectId(transaction_data['transaction_id'])})
            if not transaction:
                return {'message': "Transaction not found"}
            amount = transaction['amount']
            if transaction['type']=="credit":
                amount=-amount
            user_id = transaction_data['user_id']
            result=mongo.db.transactions.delete_one({'_id':ObjectId(transaction_data['transaction_id'])})
            amount_update=mongo.db.users.update_one(
                {"_id":ObjectId(user_id)},
                {'$inc': {'totalAmount': amount}}
            )
            if result.deleted_count==0:
                return {'message':"transaction not found"}
            return {'message':'success'}
        except Exception as e:
            return {'message':str(e)} 

    def edit_transaction_model(self,transaction_data):
        try:
            transaction=mongo.db.transactions.find_one({"_id":ObjectId(transaction_data['transaction_id'])})
            if not transaction:
                return {"message":"Transaction not found"}
            amount=transaction['amount']
            type=transaction['type']
            if type=="credit":
                amount=-amount 
            if transaction_data['type']=='credit':
                amount+=float(transaction_data['amount'])
            else:
                amount-=float(transaction_data['amount'])
            mongo.db.users.update_one({"_id":ObjectId(transaction_data['user_id'])},{'$inc':{"totalAmount":amount}})
            update_data = {
                "description": transaction_data["description"],
                "amount": float(transaction_data["amount"]),
                "type": transaction_data["type"],
                "category_id": transaction_data["category_id"],
                "date": datetime.now(timezone.utc)
            }
            result = mongo.db.transactions.update_one(
                {"_id": ObjectId(transaction_data['transaction_id']),"user_id":transaction_data['user_id']},
                {"$set":update_data}
            )
            if result.matched_count==0:
                return {"message":"fail"}
            return {'message':'success'}
        except Exception as e:
            return {'message':str(e)}