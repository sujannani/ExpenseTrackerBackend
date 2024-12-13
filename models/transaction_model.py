from dateutil import parser
from datetime import datetime,timedelta
import dateutil.parser
from app import mongo
class transaction_model:
    def add_transaction_model(self,transaction_data):
        try:
            transaction_data['date'] = parser.isoparse(transaction_data['date'])
            transaction_data['amount'] = float(transaction_data['amount'])
            transaction=mongo.db.transactions.insert_one(transaction_data)
            return {"message":'ok','transaction_id':str(transaction.inserted_id)}
        except Exception as e:
            return {'message':str(e)}
    
    def get_monthly_transactions_model(self,input_data):
        try:
            start_date =dateutil.parser.parse(input_data['start_date'])
            end_date = dateutil.parser.parse(input_data['end_date'])
            transactions = list(mongo.db.transactions.find({
                'user_id': input_data['user_id'],
                'date': {
                    '$gte': start_date,
                    '$lt': end_date
                }
            }))
            start_date_parsed = dateutil.parser.parse(input_data['start_date'])
            timezone_offset = start_date_parsed.utcoffset()
            offset_hours = timezone_offset.seconds // 3600
            offset_minutes = (timezone_offset.seconds // 60) % 60
            for transaction in transactions:
                transaction['_id']=str(transaction['_id'])
                transaction['date'] = (transaction['date'] + timedelta(hours=offset_hours, minutes=offset_minutes)).isoformat()
            return {'transactions':transactions,'message':'ok'}
        except Exception as e:
            return {'message':str(e)}
    
    def get_category_monthly_transactions_model(self,input_data):
        try:
            start_date = dateutil.parser.parse(input_data['start_date'])
            end_date = dateutil.parser.parse(input_data['end_date'])
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
                        'total_cost': {'$sum': '$amount'}
                    }
                }
            ]))            
            return {'category_transactions': transactions}
        except Exception as e:
            return {'message':str(e)}
