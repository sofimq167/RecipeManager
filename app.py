from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import User
from utils import login_required
from config import Config

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
    return render_template('dashboard.html', user_name=session.get('user_name'))

@app.route('/logout')
def logout():
    session.clear()
    #flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)