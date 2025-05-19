from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import User, Recipe, Tag
from utils import login_required
from config import Config
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    # Si el usuario ya tiene una sesión activa, redireccionar al dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    # Si no hay sesión activa, mostrar la landing page
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
            
            flash(f'Bienvenido, {user.name}!', 'success')
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
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        cooking_time = float(request.form.get('cooking_time', 0))
        servings = int(request.form.get('servings', 1))
        difficulty_level = int(request.form.get('difficulty_level', 1))
        image_url = request.form.get('image_url', '')
        
        # Procesar pasos de la receta (pueden venir múltiples campos con el mismo nombre)
        steps = []
        step_count = 1
        while True:
            step = request.form.get(f'step_{step_count}')
            if not step:
                break
            steps.append(step)
            step_count += 1
        
        # Procesar etiquetas seleccionadas
        tag_ids = request.form.getlist('tag_ids')
        
        # Crear la receta
        recipe = Recipe(
            title=title,
            description=description,
            cooking_time=cooking_time,
            servings=servings,
            difficulty_level=difficulty_level,
            image_url=image_url,
            steps=steps,
            user_id=user_id,
            tag_ids=tag_ids
        )
        
        recipe.save()
        flash('Receta creada correctamente', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_recipe.html', 
                          user_name=session.get('user_name'),
                          tags=user_tags)

@app.route('/recipes/<recipe_id>')
@login_required
def view_recipe(recipe_id):
    user_id = session.get('user_id')
    recipe = Recipe.find_by_id(recipe_id)
    
    if not recipe or str(recipe.user_id) != user_id:
        flash('Receta no encontrada', 'danger')
        return redirect(url_for('dashboard'))
    
    # Obtener las etiquetas asociadas a la receta
    recipe_tags = []
    for tag_id in recipe.tag_ids:
        tag = Tag.find_by_id(tag_id)
        if tag:
            recipe_tags.append(tag)
    
    return render_template('view_recipe.html', 
                          user_name=session.get('user_name'),
                          recipe=recipe,
                          tags=recipe_tags)

@app.route('/recipes/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    user_id = session.get('user_id')
    Recipe.collection.delete_one({'_id': ObjectId(recipe_id), 'user_id': ObjectId(user_id)})
    flash('Receta eliminada correctamente', 'success')
    return redirect(url_for('dashboard'))

@app.template_filter('format_date')
def format_date(date):
    if isinstance(date, datetime):
        return date.strftime('%d/%m/%Y')
    return ''

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)