# House of God Church

This is both frontend and backend repository for the House of God Church web application. The project provides core server-side functionality to manage church operations, user interactions, and digital resources.

## Features

- User authentication and management
- Media and static file handling
- Modular Django app structure
- Database integration (SQLite by default)
- API endpoints for frontend consumption
- Template rendering for server-side web pages

## Project Structure

- `HOG_BACKEND/` – Main Django project folder containing core settings and configuration.
- `hog/` – (Likely) main application module with models, views, and business logic.
- `media/` – Stores user-uploaded media files.
- `static/` – Stores static assets such as CSS, JS, and images.
- `templates/` – HTML templates for server-side rendering.
- `db.sqlite3` – Default SQLite database file.
- `manage.py` – Django management script.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 3.x or 4.x

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EmmanuelAyanleye/House-of-God-Church-Backend.git
   cd House-of-God-Church-Backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the backend at `http://127.0.0.1:8000/`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

