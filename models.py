from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    additional_images = db.Column(db.Text)  # JSON string of additional image URLs
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    stock_quantity = db.Column(db.Integer, default=1)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_additional_images(self):
        if self.additional_images:
            import json
            try:
                return json.loads(self.additional_images)
            except:
                return []
        return []

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def init_sample_data():
    """Initialize the database with sample handmade products"""
    import json
    
    # Create categories
    categories_data = [
        {"name": "Jewelry", "description": "Handcrafted jewelry pieces"},
        {"name": "Pottery", "description": "Ceramic and pottery items"},
        {"name": "Textiles", "description": "Handwoven fabrics and clothing"},
        {"name": "Woodwork", "description": "Carved wood items and furniture"}
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()
        categories[cat_data["name"]] = category.id
    
    # Create products
    products_data = [
        {
            "name": "Handcrafted Silver Pendant",
            "description": "Beautiful silver pendant necklace with intricate Celtic knotwork design. Each piece is hand-forged by skilled artisans using traditional techniques. Made from 925 sterling silver with an oxidized finish to highlight the detailed patterns.",
            "price": 89.99,
            "image_url": "/static/images/products/jewelry1.jpg",
            "additional_images": json.dumps(["/static/images/products/jewelry2.jpg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 5,
            "featured": True
        },
        {
            "name": "Artisan Ceramic Bowl Set",
            "description": "Set of three handmade ceramic bowls in earth tones. Perfect for serving or as decorative pieces. Each bowl is wheel-thrown and glazed with a unique reactive glaze that creates beautiful color variations.",
            "price": 124.99,
            "image_url": "/static/images/products/pottery1.jpg",
            "additional_images": json.dumps(["/static/images/products/pottery2.jpg"]),
            "category_id": categories["Pottery"],
            "stock_quantity": 3,
            "featured": True
        },
        {
            "name": "Hand-woven Wool Scarf",
            "description": "Luxurious hand-woven wool scarf in traditional patterns. Made from locally sourced wool and dyed with natural plant-based dyes. Soft, warm, and perfect for any season.",
            "price": 78.50,
            "image_url": "/static/images/products/textiles1.jpg",
            "additional_images": json.dumps(["/static/images/products/textiles2.jpg"]),
            "category_id": categories["Textiles"],
            "stock_quantity": 8,
            "featured": False
        },
        {
            "name": "Carved Wooden Jewelry Box",
            "description": "Elegant jewelry box hand-carved from sustainable hardwood. Features multiple compartments and a soft velvet lining. The intricate floral design is carved entirely by hand using traditional woodworking tools.",
            "price": 156.00,
            "image_url": "/static/images/products/woodwork1.jpg",
            "additional_images": json.dumps(["/static/images/products/woodwork2.jpg"]),
            "category_id": categories["Woodwork"],
            "stock_quantity": 2,
            "featured": True
        }
    ]
    
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
