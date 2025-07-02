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

## Changelog

Changelog:
- July 02, 2025. Initial setup