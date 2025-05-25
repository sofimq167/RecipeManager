from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import User, Recipe, Tag, Ingredient, IngredientAmount
from utils import login_required
from config import Config
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():

    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # Verificar si el usuario ya existe
        existing_user = User.find_by_email(email)
        if existing_user:
            flash('Ya existe un usuario con ese correo electrónico', 'danger')
            return render_template('register.html')
        
        # Crear nuevo usuario
        user = User(email=email, password=password, name=name)
        user_id = user.save()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.find_by_email(email)
        if user and User.check_password(user.password, password):
            # Guardar ID de usuario en la sesión
            session['user_id'] = str(user._id)
            session['user_name'] = user.name
            
            #flash(f'Bienvenido, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener las recetas del usuario actual
    user_id = session.get('user_id')
    recipes = Recipe.find_by_user_id(user_id)
    
    return render_template('dashboard.html', 
                          user_name=session.get('user_name'),
                          recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    #flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

# Rutas para gestionar etiquetas
@app.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        tag_name = request.form.get('tag_name')
        if tag_name:
            # Crear nueva etiqueta
            tag = Tag(name=tag_name, user_id=user_id)
            tag.save()
            flash('Etiqueta creada correctamente', 'success')
        else:
            flash('El nombre de la etiqueta no puede estar vacío', 'danger')
            
    # Obtener todas las etiquetas del usuario
    user_tags = Tag.find_by_user_id(user_id)
    
    return render_template('tags.html', 
                          user_name=session.get('user_name'),
                          tags=user_tags)

@app.route('/tags/delete/<tag_id>')
@login_required
def delete_tag(tag_id):
    user_id = session.get('user_id')
    Tag.collection.delete_one({'_id': ObjectId(tag_id), 'user_id': ObjectId(user_id)})
    flash('Etiqueta eliminada correctamente', 'success')
    return redirect(url_for('tags'))

# Rutas para gestionar recetas
@app.route('/recipes/create', methods=['GET', 'POST'])
@login_required
def create_recipe():
    user_id = session.get('user_id')
    user_tags = Tag.find_by_user_id(user_id)
    user_ingredients = Ingredient.find_by_user_id(user_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        cooking_time = float(request.form.get('cooking_time', 0))
        servings = int(request.form.get('servings', 1))
        difficulty_level = int(request.form.get('difficulty_level', 1))
        image_url = request.form.get('image_url', '')
        tag_ids = request.form.getlist('tag_ids')

        # Pasos
        steps = []
        step_count = 1
        while True:
            step = request.form.get(f'step_{step_count}')
            if not step:
                break
            steps.append(step)
            step_count += 1

        # Ingredientes y cantidades
        ingredient_amount_ids = []
        index = 0
        while True:
            ing_id = request.form.get(f'ingredient_{index}')
            amount = request.form.get(f'amount_{index}')
            if not ing_id or not amount:
                break
            ingredient_amount = IngredientAmount(
                ingredient_id=ing_id,
                amount=amount
            )
            ingredient_amount.save()
            ingredient_amount_ids.append(str(ingredient_amount._id))
            index += 1

        recipe = Recipe(
            title=title,
            description=description,
            cooking_time=cooking_time,
            servings=servings,
            difficulty_level=difficulty_level,
            image_url=image_url,
            steps=steps,
            user_id=user_id,
            ingredient_amount_ids=ingredient_amount_ids,
            tag_ids=tag_ids
        )
        recipe.save()
        for ia_id in ingredient_amount_ids:
            IngredientAmount.collection.update_one(
                {'_id': ObjectId(ia_id)},
                {'$set': {'recipe_id': ObjectId(recipe._id)}}
            )

        flash('Receta creada correctamente', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_recipe.html',
                           user_name=session.get('user_name'),
                           tags=user_tags,
                           ingredients=user_ingredients)

def get_conversion_factor(unit, amount):
    try:
        amount = float(amount)
    except:
        return 1.0

    if unit == 'g' or unit == 'ml':
        return amount / 100.0
    elif unit in ['taza', 'cdta', 'cda', 'unidad']:
        return amount / 1.0
    else:
        return 1.0

@app.route('/recipes/<recipe_id>')
@login_required
def view_recipe(recipe_id):
    user_id = session.get('user_id')
    recipe = Recipe.find_by_id(recipe_id)

    if not recipe or str(recipe.user_id) != user_id:
        flash('Receta no encontrada', 'danger')
        return redirect(url_for('dashboard'))
    recipe_tags = []
    for tag_id in recipe.tag_ids:
        tag = Tag.find_by_id(tag_id)
        if tag:
            recipe_tags.append(tag)
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0
    total_calories = 0.0
    ingredient_details = []

    for ia_id in recipe.ingredient_amount_ids:
        ing_amt = IngredientAmount.collection.find_one({'_id': ObjectId(ia_id)})
        if ing_amt:
            ingredient = Ingredient.collection.find_one({'_id': ing_amt['ingredient_id']})
            if ingredient:
                unit = ingredient.get('unit', 'g')
                amount = ing_amt.get('amount', 0)

                factor = get_conversion_factor(unit, amount)

                protein = ingredient.get('protein', 0.0) * factor
                carbs = ingredient.get('carbs', 0.0) * factor
                fat = ingredient.get('fat', 0.0) * factor
                calories = (protein * 4) + (carbs * 4) + (fat * 9)

                total_protein += protein
                total_carbs += carbs
                total_fat += fat
                total_calories += calories

                ingredient_details.append({
                    'name': ingredient['name'],
                    'unit': unit,
                    'amount': amount,
                    'protein': round(protein, 2),
                    'carbs': round(carbs, 2),
                    'fat': round(fat, 2),
                    'calories': round(calories, 2)
                })

    return render_template(
        'view_recipe.html',
        user_name=session.get('user_name'),
        recipe=recipe,
        tags=recipe_tags,
        total_protein=round(total_protein, 2),
        total_carbs=round(total_carbs, 2),
        total_fat=round(total_fat, 2),
        total_calories=round(total_calories, 2),
        ingredient_details=ingredient_details
    )


@app.route('/recipes/edit/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    user_id = session.get('user_id')
    recipe = Recipe.find_by_id(recipe_id)

    if not recipe or str(recipe.user_id) != user_id:
        flash('No tienes permiso para editar esta receta', 'danger')
        return redirect(url_for('dashboard'))

    tags = Tag.find_by_user_id(user_id)
    ingredients = Ingredient.find_by_user_id(user_id)
    ingredient_amounts = IngredientAmount.find_by_recipe_id(recipe._id)

    if request.method == 'POST':
        IngredientAmount.delete_by_recipe_id(recipe._id)

        title = request.form.get('title')
        description = request.form.get('description')
        cooking_time = float(request.form.get('cooking_time', 0))
        servings = int(request.form.get('servings', 1))
        difficulty_level = int(request.form.get('difficulty_level', 1))
        image_url = request.form.get('image_url', '')
        tag_ids = request.form.getlist('tag_ids')

        # Pasos
        steps = []
        step_index = 1
        while True:
            step = request.form.get(f'step_{step_index}')
            if not step:
                break
            steps.append(step)
            step_index += 1

        # Ingredientes nuevos
        ingredient_amount_ids = []
        index = 0
        while True:
            ing_id = request.form.get(f'ingredient_{index}')
            amount = request.form.get(f'amount_{index}')
            if not ing_id or not amount:
                break
            ingredient_amount = IngredientAmount(
                ingredient_id=ing_id,
                amount=amount,
                recipe_id=recipe._id
            )
            ingredient_amount.save()
            ingredient_amount_ids.append(str(ingredient_amount._id))
            index += 1

        recipe.title = title
        recipe.description = description
        recipe.cooking_time = cooking_time
        recipe.servings = servings
        recipe.difficulty_level = difficulty_level
        recipe.image_url = image_url
        recipe.steps = steps
        recipe.tag_ids = tag_ids
        recipe.ingredient_amount_ids = ingredient_amount_ids
        recipe.save()

        flash('Receta actualizada correctamente', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe._id))

    return render_template('edit_recipe.html',
                           user_name=session.get('user_name'),
                           recipe=recipe,
                           tags=tags,
                           ingredients=ingredients,
                           ingredient_amounts=ingredient_amounts)

@app.template_filter('format_date')
def format_date(date):
    if isinstance(date, datetime):
        return date.strftime('%d/%m/%Y')
    return ''

@app.route('/recipes/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    user_id = session.get('user_id')

    recipe = Recipe.find_by_id(recipe_id)
    if not recipe or str(recipe.user_id) != user_id:
        flash("No tienes permiso para eliminar esta receta", "danger")
        return redirect(url_for("dashboard"))

    # Elimina la receta
    Recipe.collection.delete_one({"_id": ObjectId(recipe_id), "user_id": ObjectId(user_id)})

    # Elimina también las cantidades de ingredientes asociadas
    IngredientAmount.delete_by_recipe_id(recipe_id)

    flash("Receta eliminada correctamente", "success")
    return redirect(url_for("dashboard"))

@app.route('/ingredients')
@login_required
def ingredients():
    user_id = session.get('user_id')
    user_ingredients = Ingredient.find_by_user_id(user_id)
    return render_template('ingredients.html',
                           user_name=session.get('user_name'),
                           ingredients=user_ingredients)


@app.route('/ingredients/create', methods=['POST'])
@login_required
def create_ingredient():
    user_id = session.get('user_id')
    name = request.form.get('name')
    unit = request.form.get('unit')
    protein = float(request.form.get('protein', 0))
    carbs = float(request.form.get('carbs', 0))
    fat = float(request.form.get('fat', 0))

    if not name or not unit:
        flash('El nombre y la unidad son obligatorios.', 'danger')
        return redirect(url_for('ingredients'))

    ingredient = Ingredient(
        name=name,
        unit=unit,
        protein=protein,
        carbs=carbs,
        fat=fat,
        user_id=user_id
    )
    ingredient.save()

    flash('Ingrediente creado correctamente.', 'success')
    return redirect(url_for('ingredients'))

@app.route('/ingredients/edit', methods=['POST'])
@login_required
def edit_ingredient():
    ingredient_id = request.form.get('ingredient_id')
    name = request.form.get('name')
    unit = request.form.get('unit')
    protein = float(request.form.get('protein', 0))
    carbs = float(request.form.get('carbs', 0))
    fat = float(request.form.get('fat', 0))

    ingredient = Ingredient.find_by_id(ingredient_id)
    if ingredient:
        ingredient.name = name
        ingredient.unit = unit
        ingredient.protein = protein
        ingredient.carbs = carbs
        ingredient.fat = fat
        ingredient.save()
        flash('Ingrediente actualizado correctamente.', 'success')
    else:
        flash('Ingrediente no encontrado.', 'danger')

    return redirect(url_for('ingredients'))

@app.route('/ingredients/delete/<ingredient_id>')
@login_required
def delete_ingredient(ingredient_id):
    Ingredient.collection.delete_one({'_id': ObjectId(ingredient_id)})
    flash('Ingrediente eliminado correctamente.', 'success')
    return redirect(url_for('ingredients'))


from models import RecetaMealPrep, MealPrep  # Asegúrate de importar

@app.route('/meal-prep/create', methods=['GET', 'POST'])
@login_required
def create_meal_prep():
    user_id = session.get('user_id')
    user_recipes = Recipe.find_by_user_id(user_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash('El nombre del meal prep es obligatorio', 'danger')
            return render_template('create_meal_prep.html',
                                   user_name=session.get('user_name'),
                                   recipes=user_recipes)
        
        # Crear el meal prep
        meal_prep = MealPrep(user_id=user_id, name=name)
        meal_prep.save()
        
        # Obtener todas las asignaciones del formulario
        receta_meal_prep_ids = []
        days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        
        for day in days:
            # Verificar cada tipo de comida para este día
            moments = ['desayuno', 'snack1', 'snack2', 'snack3', 'almuerzo', 'cena']
            
            for moment in moments:
                # Obtener múltiples recetas para este momento (array)
                recipe_ids = request.form.getlist(f'{day}_{moment}[]')
                for recipe_id in recipe_ids:
                    if recipe_id:  # Si se seleccionó una receta para este momento
                        receta_meal_prep = RecetaMealPrep(
                            recipe_id=recipe_id,
                            day=day,
                            moment=moment,
                            meal_prep_id=meal_prep._id
                        )
                        receta_meal_prep.save()
                        receta_meal_prep_ids.append(str(receta_meal_prep._id))
        
        # Actualizar el meal prep con los IDs de RecetaMealPrep
        meal_prep.receta_meal_prep_ids = receta_meal_prep_ids
        meal_prep.save()
        
        flash('¡Meal Prep creado exitosamente!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_meal_prep.html',
                           user_name=session.get('user_name'),
                           recipes=user_recipes)


@app.route('/meal-prep')
@login_required
def meal_prep_list():
    user_id = session.get('user_id')
    meal_preps = MealPrep.find_by_user_id(user_id)
    
    return render_template('meal_prep_list.html',
                           user_name=session.get('user_name'),
                           meal_preps=meal_preps)

@app.route('/meal-prep/<meal_prep_id>')
@login_required
def view_meal_prep(meal_prep_id):
    user_id = session.get('user_id')
    meal_prep = MealPrep.find_by_id(meal_prep_id)

    if not meal_prep or str(meal_prep.user_id) != user_id:
        flash('Meal Prep no encontrado', 'danger')
        return redirect(url_for('meal_prep_list'))

    receta_meal_preps = RecetaMealPrep.find_by_meal_prep_id(meal_prep._id)

    days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    moments = ['desayuno', 'snack1', 'almuerzo', 'snack2', 'cena', 'snack3']

    meal_plan = {}
    for day in days:
        meal_plan[day] = {}
        for moment in moments:
            meal_plan[day][moment] = []

    for rmp in receta_meal_preps:
        recipe = Recipe.find_by_id(rmp.recipe_id)
        if recipe:
            meal_plan[rmp.day][rmp.moment].append({
                'recipe': recipe,
                'recipe_id': str(recipe._id)
            })

    # Calcular macros por día
    from collections import defaultdict
    from models import IngredientAmount, Ingredient

    def get_conversion_factor(unit, amount):
        try:
            amount = float(amount)
        except:
            return 1.0
        return amount / 100.0 if unit in ['g', 'ml'] else 1.0

    day_macros = defaultdict(lambda: {'protein': 0.0, 'carbs': 0.0, 'fat': 0.0})

    for day in days:
        for moment in moments:
            for item in meal_plan[day][moment]:
                recipe = item['recipe']
                for ia_id in recipe.ingredient_amount_ids:
                    ing_amt = IngredientAmount.collection.find_one({'_id': ObjectId(ia_id)})
                    if not ing_amt:
                        continue
                    ingredient = Ingredient.collection.find_one({'_id': ing_amt['ingredient_id']})
                    if not ingredient:
                        continue
                    unit = ingredient.get('unit', 'g')
                    amount = ing_amt.get('amount', 0)
                    factor = get_conversion_factor(unit, amount)
                    day_macros[day]['protein'] += ingredient.get('protein', 0.0) * factor
                    day_macros[day]['carbs'] += ingredient.get('carbs', 0.0) * factor
                    day_macros[day]['fat'] += ingredient.get('fat', 0.0) * factor

    return render_template('view_meal_prep.html',
                           user_name=session.get('user_name'),
                           meal_prep=meal_prep,
                           meal_plan=meal_plan,
                           days=days,
                           day_macros=day_macros)


@app.route('/meal-prep/edit/<meal_prep_id>', methods=['GET', 'POST'])
@login_required
def edit_meal_prep(meal_prep_id):
    user_id = session.get('user_id')
    meal_prep = MealPrep.find_by_id(meal_prep_id)
    
    if not meal_prep or str(meal_prep.user_id) != user_id:
        flash('No tienes permiso para editar este meal prep', 'danger')
        return redirect(url_for('meal_prep_list'))
    
    user_recipes = Recipe.find_by_user_id(user_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash('El nombre del meal prep es obligatorio', 'danger')
            return render_template('edit_meal_prep.html',
                                   user_name=session.get('user_name'),
                                   recipes=user_recipes,
                                   meal_prep=meal_prep)
        
        # Eliminar las RecetaMealPrep existentes
        RecetaMealPrep.delete_by_meal_prep_id(meal_prep._id)
        
        # Actualizar el nombre del meal prep
        meal_prep.name = name
        
        # Crear nuevas asignaciones del formulario
        receta_meal_prep_ids = []
        days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        
        for day in days:
            moments = ['desayuno', 'snack1', 'snack2', 'snack3', 'almuerzo', 'cena']
            
            for moment in moments:
                recipe_ids = request.form.getlist(f'{day}_{moment}[]')
                for recipe_id in recipe_ids:
                    if recipe_id:
                        receta_meal_prep = RecetaMealPrep(
                            recipe_id=recipe_id,
                            day=day,
                            moment=moment,
                            meal_prep_id=meal_prep._id
                        )
                        receta_meal_prep.save()
                        receta_meal_prep_ids.append(str(receta_meal_prep._id))
        
        # Actualizar el meal prep con los nuevos IDs
        meal_prep.receta_meal_prep_ids = receta_meal_prep_ids
        meal_prep.save()
        
        flash('¡Meal Prep actualizado exitosamente!', 'success')
        return redirect(url_for('view_meal_prep', meal_prep_id=meal_prep._id))
    
    # Para GET: obtener las RecetaMealPrep existentes
    receta_meal_preps = RecetaMealPrep.find_by_meal_prep_id(meal_prep._id)
    
    # Organizar las recetas por día y momento
    days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    moments = ['desayuno', 'snack1', 'almuerzo', 'snack2', 'cena', 'snack3']
    
    current_meal_data = {}
    for day in days:
        current_meal_data[day] = {}
        for moment in moments:
            current_meal_data[day][moment] = []
    
    # Llenar con los datos actuales
    for rmp in receta_meal_preps:
        current_meal_data[rmp.day][rmp.moment].append(str(rmp.recipe_id))
    
    return render_template('edit_meal_prep.html',
                           user_name=session.get('user_name'),
                           recipes=user_recipes,
                           meal_prep=meal_prep,
                           current_meal_data=current_meal_data)

@app.route('/meal-prep/delete/<meal_prep_id>')
@login_required
def delete_meal_prep(meal_prep_id):
    user_id = session.get('user_id')
    
    # Verificar que el meal prep existe y pertenece al usuario
    meal_prep = MealPrep.find_by_id(meal_prep_id)
    if not meal_prep or str(meal_prep.user_id) != user_id:
        flash("No tienes permiso para eliminar este meal prep", "danger")
        return redirect(url_for("meal_prep_list"))
    
    # Eliminar todas las RecetaMealPrep asociadas
    RecetaMealPrep.delete_by_meal_prep_id(meal_prep._id)
    
    # Eliminar el meal prep
    MealPrep.collection.delete_one({"_id": ObjectId(meal_prep_id), "user_id": ObjectId(user_id)})
    
    flash("Meal Prep eliminado correctamente", "success")
    return redirect(url_for("meal_prep_list"))

if __name__ == '__main__':
    #app.run(debug=Config.DEBUG)
    app.run(debug=True)