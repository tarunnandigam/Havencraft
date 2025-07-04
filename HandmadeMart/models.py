from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .app import db

# Create a mapping of category names to their IDs for easy reference
category_map = {}

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def init_db():
    """Initialize the database with sample data"""
    # Only initialize if no categories exist
    if not Category.query.first():
        init_categories()
        init_products()

def init_categories():
    """Initialize categories in the database"""
    categories = [
        ("Jewelry", "Handcrafted jewelry pieces"),
        ("Pottery", "Ceramic and pottery items"),
        ("Textiles", "Handwoven and dyed fabrics"),
        ("Woodwork", "Hand-carved wooden items"),
        ("Glass", "Hand-blown glass items"),
        ("Home Decor", "Decorative items for your home")
    ]
    
    for name, description in categories:
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        category_map[name.lower()] = category.id

def init_products():
    """Initialize products in the database"""
    products = [
        {
            "name": "Handmade Silver Ring",
            "description": "Beautiful silver ring with intricate designs",
            "price": 59.99,
            "image_url": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "category_id": category_map.get("jewelry", 1),
            "stock_quantity": 10,
            "featured": True
        },
        {
            "name": "Ceramic Vase",
            "description": "Hand-thrown ceramic vase with unique glaze",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1581655358543-82a0f323886c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "category_id": category_map.get("pottery", 2),
            "stock_quantity": 5,
            "featured": True
        },
        {
            "name": "Wool Scarf",
            "description": "Handwoven wool scarf in natural colors",
            "price": 45.99,
            "image_url": "https://images.unsplash.com/photo-1576561337131-b0c0ba6f915a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "category_id": category_map.get("textiles", 3),
            "stock_quantity": 15,
            "featured": True
        }
    ]
    
    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
