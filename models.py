from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from config import Config

# Conexión a MongoDB Atlas
client = MongoClient(Config.MONGO_URI)
db = client.ChefBoxDB
bcrypt = Bcrypt()

class User:
    collection = db.users
    
    def __init__(self, email, password, name, _id=None):
        self.email = email
        self.password = password
        self.name = name
        self._id = _id
    
    def save(self):
        """Guardar usuario en la base de datos"""
        if not self._id:
            # Hashear la contraseña
            hashed_pw = bcrypt.generate_password_hash(self.password).decode('utf-8')
            
            # Nuevo usuario
            user_data = {
                'email': self.email,
                'password': hashed_pw,
                'name': self.name,
                'created_at': datetime.utcnow()
            }
            
            result = self.collection.insert_one(user_data)
            self._id = result.inserted_id
            return self._id
        else:
            # Actualizar usuario existente (si es necesario)
            self.collection.update_one(
                {'_id': self._id},
                {'$set': {
                    'email': self.email,
                    'name': self.name,
                    'updated_at': datetime.utcnow()
                }}
            )
            return self._id
    
    @classmethod
    def find_by_email(cls, email):
        """Buscar usuario por email"""
        user_data = cls.collection.find_one({'email': email})
        if user_data:
            return cls(
                email=user_data['email'],
                password=user_data['password'],  # Contraseña hasheada de la BD
                name=user_data['name'],
                _id=user_data['_id']
            )
        return None
    
    @classmethod
    def find_by_id(cls, user_id):
        """Buscar usuario por ID"""
        user_data = cls.collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return cls(
                email=user_data['email'],
                password=user_data['password'],
                name=user_data['name'],
                _id=user_data['_id']
            )
        return None
    
    @staticmethod
    def check_password(hashed_password, password):
        """Verificar contraseña"""
        return bcrypt.check_password_hash(hashed_password, password)