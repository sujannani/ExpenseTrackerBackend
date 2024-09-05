from dateutil import parser
from datetime import datetime
from app import mongo
class transaction_model:
    def add_transaction_model(self,transaction_data):
        try:
            transaction_data['date'] = parser.isoparse(transaction_data['date'])
            transaction=mongo.db.transactions.insert_one(transaction_data)
            return {"message":'ok','transaction':str(transaction.inserted_id)}
        except Exception as e:
            return {'message':str(e)}
    
    def get_monthly_transactions_model(self,input_data):
        print(input_data)
        try:
            start_date = datetime.fromisoformat(input_data['start_date'])
            end_date = datetime.fromisoformat(input_data['end_date'])
            transactions = list(mongo.db.transactions.find({
                'user_id': input_data['user_id'],
                'date': {
                    '$gte': start_date,
                    '$lt': end_date
                }
            }))
            for transaction in transactions:
                transaction['_id']=str(transaction['_id'])
            return {'transactions':transactions}
        except Exception as e:
            return {'message':str(e)}
