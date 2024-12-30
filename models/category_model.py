from app import mongo
from bson import ObjectId # type: ignore
class category_model:
    def add_category_model(self,category_data):
        try:
            existing_category = mongo.db.categories.find_one({
                'user_id':category_data['user_id'],
                'active':True,
                '$or': [
                    {'category_name': category_data['category_name']},
                    {'emoji': category_data['emoji']}
                ]
            })
            if existing_category:
                return {'message':'Name or emoji already existed'}
            category_data['active']=True
            category=mongo.db.categories.insert_one(category_data)
            return {'message':'success','category_id':str(category.inserted_id)}
        except Exception as e:
            return {"message":f'something went wrong {e}'}
    
    def get_categories_model(self,user_data):
        try:
            categories=list(mongo.db.categories.find({'user_id': user_data['user_id']}))
            for cat in categories:
                cat['_id']=str(cat['_id'])
            return {'categories':categories,'message':"success"}
        except Exception as e: 
            return {'message':f'{e}','categories':{}}
    
    def delete_category_model(self,category_data):
        try:
            existing_category=mongo.db.categories.find_one({
                '_id':ObjectId(category_data['category_id'])
            })
            if not existing_category:
                return {'message':"Category not found"}
            result=mongo.db.categories.update_one(
                {'_id':ObjectId(category_data['category_id'])},
                {'$set':{'active':False}}
            )
            if result.matched_count==0:
                return {'message':'failed to delete'}
            return {'message':'success'}
        except Exception as e:
            return {'message':f'{e}'}

    def edit_category_model(self, category_data):
        try:
            existing_category = mongo.db.categories.find_one({
                'user_id': category_data['user_id'],
                'active':True,
                '$or': [
                    {'category_name': category_data['category_name']},
                    {'emoji': category_data['emoji']}
                ],
                '_id': {'$ne': ObjectId(category_data['category_id'])}
            })
            if existing_category:
                return {'message': 'Name or emoji already existed'}
            update_result = mongo.db.categories.update_one(
                {'_id': ObjectId(category_data['category_id']), 'user_id': category_data['user_id']},
                {'$set': {
                    'category_name': category_data['category_name'],
                    'emoji': category_data['emoji'],
                }}
            )
            if update_result.matched_count == 0:
                return {'message': 'Category not found'}
            return {'message': 'success'}
        except Exception as e:
            return {'message': f'Something went wrong: {e}'}

                