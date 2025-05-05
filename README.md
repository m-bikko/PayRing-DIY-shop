# PayRing E-commerce Platform

PayRing is a Flask-based e-commerce platform for selling DIY NFC ring kits. This application follows the MVC (Model-View-Controller) architecture and provides both user-facing and admin interfaces.

## Features

### User-Side Features
- Landing page with product information
- Product catalog with filtering options
- Detailed product pages for each kit type
- Interactive product customization (ring types and sizes)
- Shopping cart functionality
- Checkout process with shipping information
- Order confirmation

### Admin-Side Features
- Secure admin login
- Dashboard with sales statistics
- Order management (view, update status)
- Product management (add, edit, delete kit types)
- Ring type management (add, edit, delete)
- Ring size management (add, edit, delete)

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Charts**: Chart.js (admin dashboard)

## Project Structure

The application follows the MVC (Model-View-Controller) architecture:

- **Models**: Represent the data structure and database schema
- **Views**: Handle the presentation layer (templates, static files)
- **Controllers**: Manage the business logic and request handling

```
PayRing_Last_MVC/
├── app/
│   ├── controllers/
│   │   ├── admin.py        # Admin panel routes
│   │   ├── main.py         # Main website routes
│   │   └── shop.py         # Shop/product routes
│   ├── models/
│   │   ├── database.py     # SQLAlchemy setup
│   │   ├── order.py        # Order and OrderItem models
│   │   ├── product.py      # Product-related models (KitType, RingType, RingSize)
│   │   └── user.py         # User model for admin authentication
│   ├── views/
│   │   ├── static/         # Static assets (CSS, JS, images)
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   └── templates/      # HTML templates
│   │       ├── admin/      # Admin panel templates
│   │       ├── shop/       # Shop/product templates
│   │       └── includes/   # Reusable template parts
│   ├── config/
│   │   └── config.py       # Application configuration
│   └── __init__.py         # Application factory
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd PayRing_Last_MVC
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python run.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

### Admin Access
- Admin panel URL: `http://127.0.0.1:5000/admin`
- Default login credentials:
  - Username: `admin`
  - Password: `admin123`

## Initial Data

When the application is first run, it creates the database and automatically seeds it with the admin user. You'll need to manually create kit types, ring types, and ring sizes through the admin interface.

## Image Requirements

All images needed for the website are detailed in the `image_requirements.txt` file. These images should be placed in the appropriate subdirectories under `app/views/static/images/`.

## Development and Customization

### Adding New Kit Types
1. Log in to the admin panel
2. Navigate to "Kit Types"
3. Click "Add New Kit Type"
4. Fill in the required information and submit

### Adding New Ring Types
1. Log in to the admin panel
2. Navigate to "Ring Types"
3. Click "Add New Ring Type"
4. Fill in the required information and submit

### Adding New Ring Sizes
1. Log in to the admin panel
2. Navigate to "Ring Sizes"
3. Click "Add New Ring Size"
4. Fill in the required information and submit

### Customizing Templates
The HTML templates are located in the `app/views/templates/` directory. They use the Jinja2 templating engine and extend from base templates for consistent styling.

### Customizing Styles
The main CSS files are:
- `app/views/static/css/style.css` - For user-facing pages
- `app/views/static/css/admin.css` - For admin panel

## License

This project is licensed under the MIT License.

## Contact

For any questions or support, please contact beimbet.m04@gmail.com