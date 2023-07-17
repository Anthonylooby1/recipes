from flask import render_template, request, redirect,session, flash
from flask_app import app
from flask_app.models.users_models import User
from flask_app.models.recipes_model import Recipe

@app.route('/users/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', logged_user=logged_user, all_recipes=all_recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipes_new.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.is_valid(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create_recipe(recipe_data)
    return redirect ('/users/dashboard')

@app.route('/recipes/<int:id>')
def view_one_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    data2 = {
        'id': session['user_id']
    }
    one_user = User.get_by_id(data2)
    one_recipe = Recipe.get_one(data)
    return render_template('/recipes_one.html', one_recipe=one_recipe, one_user=one_user)

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/')

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_recipe = Recipe.get_one(data)
    return render_template('recipes_edit.html', one_recipe=one_recipe)

@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        **request.form,
        'id': id
    }
    if not Recipe.is_valid(request.form):
        return redirect(f'/recipes/{id}/edit')
    one_recipe = Recipe.get_one(data)
    Recipe.update(data)
    return redirect('/users/dashboard')