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


class Tag:
    collection = db.tags
    
    def __init__(self, name, user_id, _id=None):
        self.name = name
        self.user_id = user_id  # ID del usuario que creó la etiqueta
        self._id = _id
    
    def save(self):
        """Guardar etiqueta en la base de datos"""
        if not self._id:
            # Nueva etiqueta
            tag_data = {
                'name': self.name,
                'user_id': ObjectId(self.user_id),
                'created_at': datetime.utcnow()
            }
            
            result = self.collection.insert_one(tag_data)
            self._id = result.inserted_id
            return self._id
        else:
            # Actualizar etiqueta existente
            self.collection.update_one(
                {'_id': self._id},
                {'$set': {
                    'name': self.name,
                    'updated_at': datetime.utcnow()
                }}
            )
            return self._id
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Encontrar todas las etiquetas de un usuario"""
        cursor = cls.collection.find({'user_id': ObjectId(user_id)})
        tags = []
        for tag_data in cursor:
            tags.append(cls(
                name=tag_data['name'],
                user_id=tag_data['user_id'],
                _id=tag_data['_id']
            ))
        return tags
    
    @classmethod
    def find_by_id(cls, tag_id):
        """Buscar etiqueta por ID"""
        tag_data = cls.collection.find_one({'_id': ObjectId(tag_id)})
        if tag_data:
            return cls(
                name=tag_data['name'],
                user_id=tag_data['user_id'],
                _id=tag_data['_id']
            )
        return None


class Recipe:
    collection = db.recipes
    
    def __init__(self, title, description, cooking_time, servings, difficulty_level, 
                 image_url, steps, user_id, tag_ids=None, created_at=None, _id=None):
        self.title = title
        self.description = description
        self.cooking_time = cooking_time  # En minutos
        self.servings = servings
        self.difficulty_level = difficulty_level  # 1-5
        self.image_url = image_url
        self.steps = steps  # Lista de pasos
        self.user_id = user_id
        self.tag_ids = tag_ids or []  # Lista de IDs de etiquetas
        self.created_at = created_at or datetime.utcnow()
        self._id = _id
    
    def save(self):
        """Guardar receta en la base de datos"""
        # Convertir los IDs de etiquetas a ObjectId si son string
        tag_ids_obj = [ObjectId(tag_id) if isinstance(tag_id, str) else tag_id for tag_id in self.tag_ids]
        
        if not self._id:
            # Nueva receta
            recipe_data = {
                'title': self.title,
                'description': self.description,
                'cooking_time': self.cooking_time,
                'servings': self.servings,
                'difficulty_level': self.difficulty_level,
                'image_url': self.image_url,
                'steps': self.steps,
                'user_id': ObjectId(self.user_id),
                'tag_ids': tag_ids_obj,
                'created_at': self.created_at
            }
            
            result = self.collection.insert_one(recipe_data)
            self._id = result.inserted_id
            return self._id
        else:
            # Actualizar receta existente
            self.collection.update_one(
                {'_id': self._id},
                {'$set': {
                    'title': self.title,
                    'description': self.description,
                    'cooking_time': self.cooking_time,
                    'servings': self.servings,
                    'difficulty_level': self.difficulty_level,
                    'image_url': self.image_url,
                    'steps': self.steps,
                    'tag_ids': tag_ids_obj,
                    'updated_at': datetime.utcnow()
                }}
            )
            return self._id
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Encontrar todas las recetas de un usuario"""
        cursor = cls.collection.find({'user_id': ObjectId(user_id)})
        recipes = []
        for recipe_data in cursor:
            recipes.append(cls(
                title=recipe_data['title'],
                description=recipe_data['description'],
                cooking_time=recipe_data['cooking_time'],
                servings=recipe_data['servings'],
                difficulty_level=recipe_data['difficulty_level'],
                image_url=recipe_data['image_url'],
                steps=recipe_data['steps'],
                user_id=recipe_data['user_id'],
                tag_ids=recipe_data.get('tag_ids', []),
                created_at=recipe_data.get('created_at'),
                _id=recipe_data['_id']
            ))
        return recipes
    
    @classmethod
    def find_by_id(cls, recipe_id):
        """Buscar receta por ID"""
        recipe_data = cls.collection.find_one({'_id': ObjectId(recipe_id)})
        if recipe_data:
            return cls(
                title=recipe_data['title'],
                description=recipe_data['description'],
                cooking_time=recipe_data['cooking_time'],
                servings=recipe_data['servings'],
                difficulty_level=recipe_data['difficulty_level'],
                image_url=recipe_data['image_url'],
                steps=recipe_data['steps'],
                user_id=recipe_data['user_id'],
                tag_ids=recipe_data.get('tag_ids', []),
                created_at=recipe_data.get('created_at'),
                _id=recipe_data['_id']
            )
        return None