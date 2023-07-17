from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_models
from flask_app import DATABASE
from flask import flash

DATABASE = 'my_recipes'

class Recipe:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.instructions = data['instructions']
        self.description = data['description']
        self.under_30 = data['under_30']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def get_all_recipes(cls):
        query = """
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_recipes = []
        if results:
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = users_models.User(user_data)
                this_recipe.cook = this_user
                all_recipes.append(this_recipe)
        return all_recipes                            

    @classmethod
    def create_recipe(cls,data):
        query = """
            INSERT INTO recipes (name, instructions, description, under_30, date_cooked, user_id)
            VALUES (%(name)s, %(instructions)s, %(description)s, %(under_30)s, %(date_cooked)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data) 
    
    @classmethod
    def get_one(cls,data):
        query = """
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if results:
            row = results[0]
            for row in results:
                this_recipe = cls(row)
                user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_user = users_models.User(user_data)
            this_recipe.cook = this_user
            return this_recipe
        return False 
    

    @classmethod
    def delete(cls,data):
        query = """DELETE FROM recipes WHERE id = %(id)s"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = """
            UPDATE recipes SET 
            name = %(name)s,
            instructions = %(instructions)s,
            description = %(description)s,
            under_30 = %(under_30)s,
            date_cooked = %(date_cooked)s
            WHERE recipes.id = %(id)s;
            """
        return connectToMySQL(DATABASE).query_db(query,data)

    
    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data['name']) < 1:
            flash('name required')
            is_valid = False
        if len(data['description']) < 1:
            flash('description required')
            is_valid = False
        if len(data['instructions']) < 1:
            flash('instructions required')
            is_valid = False
        if len(data['date_cooked']) < 1:
            flash('date required')
            is_valid = False
        if 'under_30' not in data:
            flash('under 30 minutes required')
            is_valid = False
        return is_valid                   
