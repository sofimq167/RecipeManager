import os
from dotenv import load_dotenv

if os.environ.get("RENDER") != "true":
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secretita_jijiji')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://usuario:contraseña@cluster0.mongodb.net/nombre_bd')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'