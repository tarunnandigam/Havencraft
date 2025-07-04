# HavenCraft - Professional Handmade Marketplace

A modern, professional e-commerce platform for handmade products built with Flask, PostgreSQL, and Bootstrap. Inspired by leading marketplaces like Myntra and Flipkart with comprehensive e-commerce functionality.

## 🌟 Features

### Core E-commerce Functionality
- **User Authentication**: Complete registration, login, and profile management
- **Product Catalog**: 22+ handmade products across 6 categories
- **Shopping Cart**: Session-based cart with quantity management
- **Wishlist**: Save favorite products for later
- **Complete Checkout Process**: 4-step checkout with shipping, payment, and confirmation
- **Order Management**: Track orders with detailed history
- **Responsive Design**: Mobile-first design with Bootstrap 5.3.2

### Professional Features
- **Modern UI/UX**: Myntra/Flipkart-inspired design
- **PostgreSQL Database**: Production-ready database architecture
- **Secure Authentication**: Password hashing with Flask-Login
- **Real Images**: High-quality SVG product images stored locally
- **Order Tracking**: Complete order lifecycle management
- **Email Integration**: Order confirmation system ready

## 🚀 Live Demo

Visit the live application: [Your Render Deployment URL]

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/havencraft.git
cd havencraft
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost/havencraft
SESSION_SECRET=your-secret-key-here
FLASK_ENV=development
```

5. **Set up PostgreSQL database**
```bash
# Create database
createdb havencraft

# Run the application (it will create tables automatically)
python main.py
```

6. **Access the application**
Open your browser and navigate to `http://localhost:5000`

## 🌐 Deployment on Render

### Step 1: Prepare Your Repository

1. **Ensure your code is in a Git repository**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Create requirements.txt** (if not exists)
```bash
pip freeze > requirements.txt
```

### Step 2: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "PostgreSQL"
3. Configure your database:
   - **Name**: `havencraft-db`
   - **Database**: `havencraft`
   - **User**: `havencraft_user`
   - **Region**: Choose closest to your users
4. Click "Create Database"
5. **Save the connection details** provided by Render

### Step 3: Deploy Web Service

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:

#### Basic Settings
- **Name**: `havencraft`
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

#### Build & Deploy Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --reuse-port --reload main:app`

#### Environment Variables
Add these environment variables in the Render dashboard:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | [Copy from your PostgreSQL service] |
| `SESSION_SECRET` | [Generate a secure random string] |
| `FLASK_ENV` | `production` |

### Step 4: Configure Domain (Optional)

1. In your web service settings, go to "Custom Domains"
2. Add your custom domain
3. Configure DNS with your domain provider

### Step 5: Database Migration

The application automatically creates tables on first run. If you need to add sample data:

1. Access your deployed application
2. The database will be initialized with sample products automatically

## 🛠️ Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `SESSION_SECRET` | Secret key for sessions | `your-super-secret-key-here` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `PORT` | Application port | `5000` |

## 📁 Project Structure

```
havencraft/
├── app.py                 # Application factory and configuration
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # URL routes and view logic
├── auth_routes.py        # Authentication routes
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── static/              # Static assets
│   ├── css/
│   │   └── modern-style.css
│   ├── js/
│   │   ├── cart.js
│   │   └── main.js
│   └── images/
│       └── products/
│           └── real/     # Product images
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── auth/
│   ├── checkout/        # Complete checkout flow
│   └── ...
└── instance/           # Instance-specific files
```

## 🔧 Configuration

### Database Configuration

The application is configured to work with PostgreSQL in production and includes:
- Connection pooling
- Automatic reconnection
- SSL support for cloud deployments

### Security Features

- Password hashing with Werkzeug
- Secure session management
- CSRF protection ready
- SQL injection prevention with SQLAlchemy ORM

## 🎨 Customization

### Adding New Products

1. Products are automatically loaded from `models.py`
2. Add new product data to the `init_sample_data()` function
3. Restart the application to load new products

### Modifying Styles

1. Edit `static/css/modern-style.css` for custom styling
2. Colors, fonts, and layout can be customized
3. Bootstrap 5.3.2 classes available throughout

### Adding Payment Integration

The checkout process is ready for payment integration:
1. Add your payment provider credentials to environment variables
2. Implement payment processing in `routes.py` checkout functions
3. Update payment templates as needed

## 🚨 Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check your DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://username:password@host:port/database
```

**Import Errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**Static Files Not Loading**
- Check that `static/` directory is included in your repository
- Verify file paths in templates are correct

### Getting Help

1. Check the [Issues](https://github.com/yourusername/havencraft/issues) page
2. Review Render deployment logs
3. Verify all environment variables are set correctly

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, email support@havencraft.com or open an issue on GitHub.

---

**HavenCraft** - Connecting artisans with the world, one handmade treasure at a time. 🎨✨