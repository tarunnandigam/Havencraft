# HavenCraft - Professional Handmade Marketplace

## Overview

HavenCraft is a modern, professional e-commerce platform for handmade products, inspired by leading marketplaces like Myntra and Flipkart. The platform features user authentication, comprehensive product catalog with 22+ items, modern responsive design, shopping cart functionality, and deployment-ready architecture with PostgreSQL database support.

## System Architecture

Modern MVC architecture with professional e-commerce features:

- **Frontend**: Server-side rendered HTML templates with Jinja2, Bootstrap 5.3.2, modern CSS Grid/Flexbox
- **Backend**: Flask web application with SQLAlchemy ORM and Flask-Login authentication
- **Database**: PostgreSQL for production with comprehensive product catalog (22+ items, 6 categories)
- **Authentication**: User registration, login, profile management with secure password hashing
- **Session Management**: Flask sessions for cart functionality and user state
- **Design**: Myntra/Flipkart-inspired modern responsive interface

## Key Components

### Database Models (`models.py`)
- **Category**: Product categories with name and description
- **Product**: Core product model with pricing, images, stock, and category relationships
- **User**: User authentication model with password hashing (partially implemented)

### Application Structure
- **app.py**: Application factory and configuration
- **routes.py**: URL routing and view logic
- **main.py**: Application entry point
- **templates/**: Jinja2 HTML templates with inheritance
- **static/**: CSS, JavaScript, and asset files

### Core Features
- Product catalog with category filtering
- Search functionality across product names and descriptions
- Featured products display on homepage
- Product detail pages with image galleries
- Shopping cart with session-based storage
- Responsive design with Bootstrap 5

## Data Flow

1. **Product Display**: Products are fetched from database with optional category/search filtering
2. **Cart Management**: Cart items stored in browser sessionStorage, synced with server sessions
3. **Product Detail**: Individual product pages show detailed information and related products
4. **Search**: Real-time search across product catalog with query parameter persistence

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Werkzeug: WSGI utilities and password hashing

### Frontend Libraries
- Bootstrap 5.3.0: CSS framework and components
- Font Awesome 6.4.0: Icon library
- Custom CSS with earthy color scheme (browns, golds)

### Database
- SQLite: Default development database
- PostgreSQL: Production database support with automatic URL conversion

## Deployment Strategy

The application is configured for deployment on platforms like Replit with:
- Environment variable support for database URLs and session secrets
- ProxyFix middleware for proper header handling behind proxies
- Automatic database initialization with sample data
- Debug mode enabled for development

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Secret key for session management

## User Preferences

Preferred communication style: Simple, everyday language.

## Key Components

### Database Models (`models.py`)
- **Category**: Product categories with name and description
- **Product**: Core product model with pricing, images, stock, and category relationships
- **User**: User authentication model with password hashing and profile management
- **Wishlist**: User favorite products with unique constraints
- **Order**: Complete order tracking with status management
- **OrderItem**: Detailed order items with pricing history

### Application Structure
- **app.py**: Application factory and configuration
- **routes.py**: URL routing, cart, wishlist, and complete checkout flow
- **auth_routes.py**: User authentication and profile management
- **main.py**: Application entry point
- **templates/**: Jinja2 HTML templates with inheritance
- **templates/checkout/**: Complete 4-step checkout process
- **static/**: CSS, JavaScript, and high-quality SVG product images

### Core Features
- Product catalog with category filtering and search
- User registration, login, and profile management
- Shopping cart with session-based storage
- Wishlist functionality for saving favorite items
- Complete 4-step checkout process (Review → Shipping → Payment → Confirmation)
- Order management with detailed tracking and history
- Responsive design with professional e-commerce interface
- Real product images stored locally for deployment

## Data Flow

1. **User Authentication**: Secure registration/login with Flask-Login and password hashing
2. **Product Display**: Products fetched from PostgreSQL with filtering and search
3. **Cart Management**: Session-based cart storage with database sync for orders
4. **Wishlist System**: Database-stored user favorites with real-time updates
5. **Checkout Process**: Multi-step flow with shipping, payment, and order confirmation
6. **Order Tracking**: Complete order lifecycle from confirmation to delivery status

## External Dependencies

### Python Packages
- Flask: Web framework and routing
- Flask-SQLAlchemy: Database ORM and migrations
- Flask-Login: User session management and authentication
- Werkzeug: Password hashing and security utilities
- Gunicorn: Production WSGI server
- psycopg2-binary: PostgreSQL database adapter

### Frontend Libraries
- Bootstrap 5.3.2: CSS framework and responsive components
- Font Awesome 6.4.0: Professional icon library
- Custom CSS with modern e-commerce design patterns

### Database
- PostgreSQL: Production database with comprehensive schema
- SQLite: Development database support

## Deployment Strategy

The application is fully configured for deployment on platforms like Render with:
- Environment variable support for secure configuration
- PostgreSQL database with connection pooling
- ProxyFix middleware for proper header handling behind proxies
- Automatic database initialization with comprehensive sample data
- Gunicorn WSGI server configuration
- Real images stored locally for reliable deployment

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secure session encryption key

## Recent Changes

**July 02, 2025 - Major Feature Implementation:**
- ✅ Complete user authentication system with profiles
- ✅ Comprehensive wishlist functionality
- ✅ 4-step checkout process (Review → Shipping → Payment → Confirmation)
- ✅ Order management and tracking system
- ✅ Professional navigation with user account features
- ✅ Real product images in separate folder structure
- ✅ Complete README with deployment instructions for PostgreSQL and Render
- ✅ Modern e-commerce UI matching Myntra/Flipkart design standards

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

- July 02, 2025: Initial project setup with basic e-commerce structure
- July 02, 2025: Complete feature implementation - cart, wishlist, checkout, orders, deployment-ready