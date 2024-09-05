from app import mongo
from bson import ObjectId # type: ignore
class category_model:
    def add_category_model(self,category_data):
        try:
            existing_category = mongo.db.categories.find_one({
                'user_id':category_data['user_id'],
                '$or': [
                    {'category_name': category_data['category_name']},
                    {'emoji': category_data['emoji']}
                ]
            })
            if existing_category:
                return {'message':'Name or emoji already existed'}
            category=mongo.db.categories.insert_one(category_data)
            return {'message':'ok','category_id':str(category.inserted_id)}
        except Exception as e:
            return {"message":'not ok','error':str(e)}
    
    def get_categories_model(self,user_id):
        try:
            categories=list(mongo.db.categories.find({'user_id': user_id}))
            for cat in categories:
                cat['_id']=str(cat['_id'])
            return {'categories':categories}
        except Exception as e:
            return {'message':'not ok','error':str(e)}
    
    def edit_category_model(self,category_data):
        try:
            existing_category = mongo.db.categories.find_one({
                'user_id':category_data['user_id'],
                '$and': [
                    {'category_name': category_data['category_name']},
                    {'emoji': category_data['emoji']}
                ]
            })
            if existing_category:
                return {'message':'Name or emoji already existed'}
            result = mongo.db.categories.update_one(
                {'_id': ObjectId(category_data['category_id'])},
                {'$set': {'emoji': category_data['emoji'], 'category_name': category_data['category_name']}}
            )
            return {'message':'ok'}
        except Exception as e:
            return {'message':str(e)}
            