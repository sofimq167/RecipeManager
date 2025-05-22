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


class Ingredient:
    collection = db.ingredients
    
    def __init__(self, name, unit, protein, carbs, fat, user_id, _id=None):
        self.name = name
        self.unit = unit  # Unidad de medida (gr, tazas, etc.)
        self.protein = protein  # Gramos de proteína
        self.carbs = carbs  # Gramos de carbohidratos
        self.fat = fat  # Gramos de grasa
        self.user_id = user_id  # ID del usuario que creó el ingrediente
        self._id = _id
    
    def save(self):
        """Guardar ingrediente en la base de datos"""
        if not self._id:
            # Nuevo ingrediente
            ingredient_data = {
                'name': self.name,
                'unit': self.unit,
                'protein': self.protein,
                'carbs': self.carbs,
                'fat': self.fat,
                'user_id': ObjectId(self.user_id),
                'created_at': datetime.utcnow()
            }
            
            result = self.collection.insert_one(ingredient_data)
            self._id = result.inserted_id
            return self._id
        else:
            # Actualizar ingrediente existente
            self.collection.update_one(
                {'_id': self._id},
                {'$set': {
                    'name': self.name,
                    'unit': self.unit,
                    'protein': self.protein,
                    'carbs': self.carbs,
                    'fat': self.fat,
                    'updated_at': datetime.utcnow()
                }}
            )
            return self._id
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Encontrar todos los ingredientes de un usuario"""
        cursor = cls.collection.find({'user_id': ObjectId(user_id)})
        ingredients = []
        for ingredient_data in cursor:
            ingredients.append(cls(
                name=ingredient_data['name'],
                unit=ingredient_data['unit'],
                protein=ingredient_data['protein'],
                carbs=ingredient_data['carbs'],
                fat=ingredient_data['fat'],
                user_id=ingredient_data['user_id'],
                _id=ingredient_data['_id']
            ))
        return ingredients
    
    @classmethod
    def find_by_id(cls, ingredient_id):
        """Buscar ingrediente por ID"""
        ingredient_data = cls.collection.find_one({'_id': ObjectId(ingredient_id)})
        if ingredient_data:
            return cls(
                name=ingredient_data['name'],
                unit=ingredient_data['unit'],
                protein=ingredient_data['protein'],
                carbs=ingredient_data['carbs'],
                fat=ingredient_data['fat'],
                user_id=ingredient_data['user_id'],
                _id=ingredient_data['_id']
            )
        return None


class IngredientAmount:
    collection = db.ingredient_amounts
    
    def __init__(self, ingredient_id, amount, recipe_id=None, _id=None):
        self.ingredient_id = ingredient_id  # ID del ingrediente
        self.amount = amount  # Cantidad del ingrediente
        self.recipe_id = recipe_id  # ID de la receta (opcional para creación en lote)
        self._id = _id
    
    def save(self):
        """Guardar cantidad de ingrediente en la base de datos"""
        if not self._id:
            # Nueva cantidad de ingrediente
            ingredient_amount_data = {
                'ingredient_id': ObjectId(self.ingredient_id),
                'amount': self.amount,
                'created_at': datetime.utcnow()
            }
            
            # Si se proporciona recipe_id, guardarlo también
            if self.recipe_id:
                ingredient_amount_data['recipe_id'] = ObjectId(self.recipe_id)
                
            result = self.collection.insert_one(ingredient_amount_data)
            self._id = result.inserted_id
            return self._id
        else:
            # Actualizar cantidad de ingrediente existente
            update_data = {
                'ingredient_id': ObjectId(self.ingredient_id),
                'amount': self.amount,
                'updated_at': datetime.utcnow()
            }
            
            # Si se proporciona recipe_id, actualizarlo también
            if self.recipe_id:
                update_data['recipe_id'] = ObjectId(self.recipe_id)
                
            self.collection.update_one(
                {'_id': self._id},
                {'$set': update_data}
            )
            return self._id
    
    @classmethod
    def find_by_recipe_id(cls, recipe_id):
        """Encontrar todas las cantidades de ingredientes para una receta"""
        cursor = cls.collection.find({'recipe_id': ObjectId(recipe_id)})
        ingredient_amounts = []
        for data in cursor:
            ingredient_amounts.append(cls(
                ingredient_id=data['ingredient_id'],
                amount=data['amount'],
                recipe_id=data['recipe_id'],
                _id=data['_id']
            ))
        return ingredient_amounts
    
    @classmethod
    def delete_by_recipe_id(cls, recipe_id):
        """Eliminar todas las cantidades de ingredientes para una receta"""
        cls.collection.delete_many({'recipe_id': ObjectId(recipe_id)})


class Recipe:
    collection = db.recipes
    
    def __init__(self, title, description, cooking_time, servings, difficulty_level, 
                 image_url, steps, user_id, ingredient_amount_ids=None, tag_ids=None, created_at=None, _id=None):
        self.title = title
        self.description = description
        self.cooking_time = cooking_time  # En minutos
        self.servings = servings
        self.difficulty_level = difficulty_level  # 1-5
        self.image_url = image_url
        self.steps = steps  # Lista de pasos
        self.user_id = user_id
        self.ingredient_amount_ids = ingredient_amount_ids or []  # Lista de IDs de cantidades de ingredientes
        self.tag_ids = tag_ids or []  # Lista de IDs de etiquetas
        self.created_at = created_at or datetime.utcnow()
        self._id = _id
    
    def save(self):
        """Guardar receta en la base de datos"""
        # Convertir los IDs de etiquetas a ObjectId si son string
        tag_ids_obj = [ObjectId(tag_id) if isinstance(tag_id, str) else tag_id for tag_id in self.tag_ids]
        
        # Convertir los IDs de cantidades de ingredientes a ObjectId si son string
        ingredient_amount_ids_obj = [ObjectId(ia_id) if isinstance(ia_id, str) else ia_id for ia_id in self.ingredient_amount_ids]
        
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
                'ingredient_amount_ids': ingredient_amount_ids_obj,
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
                    'ingredient_amount_ids': ingredient_amount_ids_obj,
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
                ingredient_amount_ids=recipe_data.get('ingredient_amount_ids', []),
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
                ingredient_amount_ids=recipe_data.get('ingredient_amount_ids', []),
                tag_ids=recipe_data.get('tag_ids', []),
                created_at=recipe_data.get('created_at'),
                _id=recipe_data['_id']
            )
        return None