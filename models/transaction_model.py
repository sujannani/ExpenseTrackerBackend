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
            return {'message':"success",'category_transactions': transactions}
        except Exception as e:
            return {'message':str(e)}
    
    def get_recent_transactions_model(self,user_data):
        try:
            recent_transactions = list(mongo.db.transactions.find({
                "user_id": user_data['user_id']
            }).sort("date", -1).limit(5))
            start_date_parsed = dateutil.parser.parse(user_data['date'])
            timezone_offset = start_date_parsed.utcoffset()
            offset_hours = timezone_offset.seconds // 3600
            offset_minutes = (timezone_offset.seconds // 60) % 60
            for transaction in recent_transactions:
                transaction["_id"] = str(transaction["_id"])
                transaction['date'] = (transaction['date'] + timedelta(hours=offset_hours, minutes=offset_minutes)).isoformat()
            return {"message":"success",'transactions':recent_transactions}
        except Exception as e:
            return {'message':str(e)}