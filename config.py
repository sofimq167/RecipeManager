import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configuración de la aplicación
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secretita_jijiji')
    
    # Configuración MongoDB Atlas
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://usuario:contraseña@cluster0.mongodb.net/nombre_bd')
    
    # Otras configuraciones
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'