# E-Commerce Store

## Overview

This is a full-featured e-commerce web application built with Flask that provides both customer-facing shopping functionality and admin management capabilities. The application allows customers to browse products, add items to cart, place orders, and track their purchases, while administrators can manage products, categories, and orders through a comprehensive admin panel.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses a server-side rendered architecture with Jinja2 templates and Bootstrap for responsive UI design. The frontend follows a component-based structure with reusable templates extending a base layout. JavaScript functionality is implemented for cart management, form validation, and user interactions.

### Backend Architecture
Built on Flask with SQLAlchemy ORM for database operations. The application follows a modular structure with separate files for routes, admin functionality, models, forms, and utilities. The architecture supports both customer and admin workflows with proper separation of concerns.

**Key Components:**
- **Flask Application**: Main web framework handling HTTP requests and responses
- **SQLAlchemy Models**: Database abstraction layer with Product, Category, Order, and OrderItem entities
- **WTForms**: Form handling and validation for user inputs
- **Session Management**: Cart functionality using Flask sessions
- **Template Engine**: Jinja2 for dynamic HTML generation

### Data Storage Solutions
The application uses SQLAlchemy with support for multiple database backends, currently configured for SQLite by default with environment variable override capability. The database schema includes proper relationships between products, categories, orders, and order items.

**Database Schema:**
- **Products**: Core product information with stock tracking and category relationships
- **Categories**: Product categorization system
- **Orders**: Customer order management with status tracking
- **Order Items**: Individual items within orders with quantity and pricing

### Authentication and Authorization
Currently implements a basic admin decorator system. The admin functionality uses a simple wrapper that can be extended with proper authentication mechanisms. Session-based cart management handles user state without requiring authentication for shopping.

**Security Considerations:**
- Admin routes protected by decorator (ready for authentication integration)
- Form validation using WTForms
- SQL injection prevention through SQLAlchemy ORM
- Session security with configurable secret keys

## External Dependencies

### Frontend Libraries
- **Bootstrap 5**: Responsive UI framework with dark theme support
- **Font Awesome**: Icon library for consistent iconography
- **Custom CSS**: Application-specific styling following Bootstrap conventions

### Backend Dependencies
- **Flask**: Web framework for Python applications
- **SQLAlchemy**: Database ORM and abstraction layer
- **WTForms**: Form handling and validation library
- **Flask-WTF**: Integration between Flask and WTForms

### Database Support
- **SQLite**: Default database for development and simple deployments
- **PostgreSQL**: Production-ready option via DATABASE_URL environment variable
- **Database Migrations**: Manual schema management through SQLAlchemy

### Development Tools
- **Werkzeug**: WSGI utilities and development server
- **ProxyFix**: Middleware for handling proxy headers in production environments

### Optional Integrations
The architecture supports easy integration of additional services like payment processors, email services, and external APIs for enhanced functionality. The modular design allows for extending the application with features like user authentication, advanced inventory management, and analytics.