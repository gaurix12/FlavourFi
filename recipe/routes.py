from recipe import app, db
from flask import render_template, flash, redirect, url_for, request
from recipe.models import Recipe, User
from recipe.forms import RegisterForm, LoginForm, RecipeForm, EditForm
from flask_login import login_user, login_required, current_user, logout_user
from badge.logic import assign_badge


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, name=form.username.data)
        user_to_create.password = form.password1.data
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Account created successfully!', category='success')
        return redirect(url_for('recipes_page'))

    if form.errors != {}:
        for field, error_list in form.errors.items():
            for err_msg in error_list:
                flash(f'Error in {field}: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/recipes')
def recipes_page():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipe/<int:recipe_id>')
def view_recipe_page(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/add_recipe', methods=['POST', 'GET'])
@login_required
def add_recipe_page():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_to_create = Recipe(
            name=form.name.data,
            ingredients=form.ingredients.data,
            description=form.description.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        db.session.add(recipe_to_create)

        assign_badge(current_user)

        db.session.commit()
        flash('Recipe created successfully!', category='success')
        return redirect(url_for('recipes_page'))

    if form.errors != {}:
        for field, error_list in form.errors.items():
            for err_msg in error_list:
                flash(f'Error in {field}: {err_msg}', category='danger')

    return render_template('add_recipe.html', form=form)


@app.route('/edit_page/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_page(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != current_user.id:
        flash("You don't have permission to edit this recipe.", category='danger')
        return redirect(url_for('recipes_page'))

    form = EditForm(obj=recipe)

    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.ingredients = form.ingredients.data
        recipe.description = form.description.data
        recipe.instructions = form.instructions.data
        recipe.image_url = form.image_url.data

        db.session.commit()
        flash('Recipe updated successfully!', category='success')
        return redirect(url_for('view_recipe_page', recipe_id=recipe.id))

    if form.errors:
        for field, error_list in form.errors.items():
            for err_msg in error_list:
                flash(f'Error in {field}: {err_msg}', category='danger')

    return render_template('edit_page.html', form=form, recipe=recipe)


@app.route('/delete_recipe/<int:recipe_id>', methods=['POST','GET'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != current_user.id:
        flash("You don't have permission to delete this recipe.", category='danger')
        return redirect(url_for('recipes_page'))

    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', category='success')
    return redirect(url_for('home_page'))


@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return redirect(url_for('home_page'))

    recipes = Recipe.query.filter(Recipe.name.ilike(f"%{query}%")).all()

    return render_template('search_page.html', recipes=recipes, query=query)




