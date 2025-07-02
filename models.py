from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.username

def init_sample_data():
    """Initialize the database with sample handmade products"""
    import json
    
    # Create categories
    categories_data = [
        {"name": "Jewelry", "description": "Handcrafted jewelry pieces"},
        {"name": "Pottery", "description": "Ceramic and pottery items"},
        {"name": "Textiles", "description": "Handwoven fabrics and clothing"},
        {"name": "Woodwork", "description": "Carved wood items and furniture"},
        {"name": "Home Decor", "description": "Decorative items for your home"},
        {"name": "Art & Crafts", "description": "Artistic creations and crafts"}
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()
        categories[cat_data["name"]] = category.id
    
    # Create comprehensive product catalog
    products_data = [
        # Jewelry (6 products)
        {
            "name": "Celtic Silver Pendant",
            "description": "Sterling silver pendant with intricate Celtic knotwork. Hand-forged using traditional techniques with oxidized finish.",
            "price": 89.99,
            "image_url": "/static/images/products/jewelry1.svg",
            "additional_images": json.dumps(["/static/images/products/jewelry2.svg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 12,
            "featured": True
        },
        {
            "name": "Bohemian Gemstone Earrings",
            "description": "Handcrafted earrings featuring natural gemstones in copper wire wrapping. Each pair is unique.",
            "price": 45.99,
            "image_url": "/static/images/products/jewelry1.svg",
            "additional_images": json.dumps(["/static/images/products/jewelry2.svg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 8,
            "featured": False
        },
        {
            "name": "Artisan Gold Ring",
            "description": "14k gold ring with hand-engraved patterns. Comfortable fit with unique texture finish.",
            "price": 299.99,
            "image_url": "/static/images/products/jewelry2.svg",
            "additional_images": json.dumps(["/static/images/products/jewelry1.svg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 5,
            "featured": True
        },
        {
            "name": "Vintage Copper Bracelet",
            "description": "Handforged copper bracelet with antique patina. Adjustable size with healing properties.",
            "price": 32.50,
            "image_url": "/static/images/products/jewelry1.svg",
            "additional_images": json.dumps(["/static/images/products/jewelry2.svg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 15,
            "featured": False
        },
        {
            "name": "Pearl Drop Necklace",
            "description": "Elegant freshwater pearl necklace with silver chain. Perfect for special occasions.",
            "price": 125.00,
            "image_url": "/static/images/products/jewelry2.svg",
            "additional_images": json.dumps(["/static/images/products/jewelry1.svg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 7,
            "featured": True
        },
        {
            "name": "Turquoise Statement Ring",
            "description": "Bold turquoise ring set in sterling silver. Native American inspired design.",
            "price": 78.99,
            "image_url": "/static/images/products/jewelry1.svg",
            "additional_images": json.dumps(["/static/images/products/jewelry2.svg"]),
            "category_id": categories["Jewelry"],
            "stock_quantity": 6,
            "featured": False
        },
        
        # Pottery (4 products)
        {
            "name": "Ceramic Bowl Set",
            "description": "Set of three handmade ceramic bowls in earth tones. Wheel-thrown with reactive glaze.",
            "price": 124.99,
            "image_url": "/static/images/products/pottery1.svg",
            "additional_images": json.dumps(["/static/images/products/pottery2.svg"]),
            "category_id": categories["Pottery"],
            "stock_quantity": 10,
            "featured": True
        },
        {
            "name": "Rustic Dinner Plates",
            "description": "Set of four rustic dinner plates with natural clay finish. Dishwasher safe.",
            "price": 89.99,
            "image_url": "/static/images/products/pottery2.svg",
            "additional_images": json.dumps(["/static/images/products/pottery1.svg"]),
            "category_id": categories["Pottery"],
            "stock_quantity": 8,
            "featured": False
        },
        {
            "name": "Artisan Coffee Mugs",
            "description": "Pair of handthrown coffee mugs with comfortable handles and unique glazing.",
            "price": 45.00,
            "image_url": "/static/images/products/pottery1.svg",
            "additional_images": json.dumps(["/static/images/products/pottery2.svg"]),
            "category_id": categories["Pottery"],
            "stock_quantity": 12,
            "featured": True
        },
        {
            "name": "Decorative Ceramic Vase",
            "description": "Large decorative vase with hand-painted floral motifs. Perfect centerpiece.",
            "price": 156.50,
            "image_url": "/static/images/products/pottery2.svg",
            "additional_images": json.dumps(["/static/images/products/pottery1.svg"]),
            "category_id": categories["Pottery"],
            "stock_quantity": 4,
            "featured": True
        },
        
        # Textiles (5 products)
        {
            "name": "Hand-woven Wool Scarf",
            "description": "Luxurious hand-woven wool scarf in traditional patterns. Natural plant-based dyes.",
            "price": 78.50,
            "image_url": "/static/images/products/textiles1.svg",
            "additional_images": json.dumps(["/static/images/products/textiles2.svg"]),
            "category_id": categories["Textiles"],
            "stock_quantity": 15,
            "featured": False
        },
        {
            "name": "Alpaca Wool Blanket",
            "description": "Soft alpaca wool blanket with geometric patterns. Warm and lightweight.",
            "price": 245.00,
            "image_url": "/static/images/products/textiles2.svg",
            "additional_images": json.dumps(["/static/images/products/textiles1.svg"]),
            "category_id": categories["Textiles"],
            "stock_quantity": 6,
            "featured": True
        },
        {
            "name": "Cotton Table Runner",
            "description": "Hand-embroidered cotton table runner with traditional motifs. Machine washable.",
            "price": 52.99,
            "image_url": "/static/images/products/textiles1.svg",
            "additional_images": json.dumps(["/static/images/products/textiles2.svg"]),
            "category_id": categories["Textiles"],
            "stock_quantity": 10,
            "featured": False
        },
        {
            "name": "Silk Kimono Robe",
            "description": "Beautiful silk kimono robe with hand-painted cherry blossom design.",
            "price": 189.99,
            "image_url": "/static/images/products/textiles2.svg",
            "additional_images": json.dumps(["/static/images/products/textiles1.svg"]),
            "category_id": categories["Textiles"],
            "stock_quantity": 4,
            "featured": True
        },
        {
            "name": "Handwoven Cushion Covers",
            "description": "Set of two handwoven cushion covers with geometric patterns in natural colors.",
            "price": 68.00,
            "image_url": "/static/images/products/textiles1.svg",
            "additional_images": json.dumps(["/static/images/products/textiles2.svg"]),
            "category_id": categories["Textiles"],
            "stock_quantity": 12,
            "featured": False
        },
        
        # Woodwork (4 products)
        {
            "name": "Carved Jewelry Box",
            "description": "Elegant jewelry box hand-carved from sustainable hardwood with velvet lining.",
            "price": 156.00,
            "image_url": "/static/images/products/woodwork1.svg",
            "additional_images": json.dumps(["/static/images/products/woodwork2.svg"]),
            "category_id": categories["Woodwork"],
            "stock_quantity": 8,
            "featured": True
        },
        {
            "name": "Wooden Cutting Board",
            "description": "Premium bamboo cutting board with engraved design. Food safe and durable.",
            "price": 45.99,
            "image_url": "/static/images/products/woodwork2.svg",
            "additional_images": json.dumps(["/static/images/products/woodwork1.svg"]),
            "category_id": categories["Woodwork"],
            "stock_quantity": 15,
            "featured": False
        },
        {
            "name": "Hand-turned Wooden Bowl",
            "description": "Beautiful wooden salad bowl hand-turned from cherry wood with natural finish.",
            "price": 89.50,
            "image_url": "/static/images/products/woodwork1.svg",
            "additional_images": json.dumps(["/static/images/products/woodwork2.svg"]),
            "category_id": categories["Woodwork"],
            "stock_quantity": 6,
            "featured": True
        },
        {
            "name": "Rustic Picture Frame",
            "description": "Reclaimed wood picture frame with distressed finish. Holds 8x10 photos.",
            "price": 34.99,
            "image_url": "/static/images/products/woodwork2.svg",
            "additional_images": json.dumps(["/static/images/products/woodwork1.svg"]),
            "category_id": categories["Woodwork"],
            "stock_quantity": 20,
            "featured": False
        },
        
        # Home Decor (3 products)
        {
            "name": "Macrame Wall Hanging",
            "description": "Boho style macrame wall hanging made with natural cotton cord. Perfect wall art.",
            "price": 67.99,
            "image_url": "/static/images/products/textiles1.svg",
            "additional_images": json.dumps(["/static/images/products/textiles2.svg"]),
            "category_id": categories["Home Decor"],
            "stock_quantity": 8,
            "featured": True
        },
        {
            "name": "Ceramic Candle Holders",
            "description": "Set of three ceramic candle holders in gradient blue glaze. Creates ambient lighting.",
            "price": 42.50,
            "image_url": "/static/images/products/pottery1.svg",
            "additional_images": json.dumps(["/static/images/products/pottery2.svg"]),
            "category_id": categories["Home Decor"],
            "stock_quantity": 12,
            "featured": False
        },
        {
            "name": "Wooden Wind Chimes",
            "description": "Handcrafted bamboo wind chimes with soothing natural tones. Weather resistant.",
            "price": 38.99,
            "image_url": "/static/images/products/woodwork1.svg",
            "additional_images": json.dumps(["/static/images/products/woodwork2.svg"]),
            "category_id": categories["Home Decor"],
            "stock_quantity": 10,
            "featured": False
        }
    ]
    
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
