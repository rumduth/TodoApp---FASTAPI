# TodoApp - FastAPI Todo Application

A full-featured Todo application built with FastAPI, featuring user authentication, role-based access control, and a web interface.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Role-Based Access Control**: Admin and regular user roles
- **Todo Management**: Create, read, update, and delete todos
- **Web Interface**: HTML templates with Bootstrap styling
- **Database Support**: PostgreSQL with SQLAlchemy ORM
- **Database Migrations**: Alembic for database schema management
- **Comprehensive Testing**: Unit tests for all major components

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with bcrypt password hashing
- **Frontend**: HTML templates with Jinja2, Bootstrap CSS
- **Database Migrations**: Alembic
- **Testing**: pytest

## Project Structure

```
TodoApp/
├── main.py                 # FastAPI application entry point
├── models.py              # SQLAlchemy database models
├── database.py            # Database configuration
├── dependency.py          # Authentication and database dependencies
├── alembic.ini           # Alembic configuration
├── routers/              # API route handlers
│   ├── auth.py           # Authentication routes
│   ├── todos.py          # Todo CRUD operations
│   ├── admin.py          # Admin-only operations
│   └── users.py          # User management
├── templates/            # HTML templates
│   ├── layout.html       # Base template
│   ├── navbar.html       # Navigation component
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── todo.html         # Todo list page
│   ├── add-todo.html     # Add todo form
│   └── edit-todo.html    # Edit todo form
├── static/               # Static assets
│   ├── css/              # CSS files
│   └── js/               # JavaScript files
├── alembic/              # Database migration files
└── test/                 # Test files
```

## Database Models

### Users

- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `first_name`: User's first name
- `last_name`: User's last name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `role`: User role (admin/user)
- `phone_number`: Contact number

### Todos

- `id`: Primary key
- `title`: Todo title (minimum 3 characters)
- `description`: Todo description (3-100 characters)
- `priority`: Priority level (1-5)
- `complete`: Completion status
- `owner_id`: Foreign key to Users table

## API Endpoints

### Authentication (`/auth`)

- `GET /auth/login-page` - Login page
- `GET /auth/register-page` - Registration page
- `POST /auth/` - Create new user
- `POST /auth/token` - Login and get access token

### Todos (`/todos`)

- `GET /todos/todo-page` - Todo list page
- `GET /todos/add-todo-page` - Add todo page
- `GET /todos/edit-todo-page/{todo_id}` - Edit todo page
- `GET /todos/` - Get all user's todos (API)
- `GET /todos/todo/{todo_id}` - Get specific todo (API)
- `POST /todos/create-todo` - Create new todo
- `PUT /todos/todo/{todo_id}` - Update todo
- `DELETE /todos/todo/{todo_id}` - Delete todo

### Admin (`/admin`)

- `GET /admin/todo` - Get all todos (admin only)
- `DELETE /admin/todo/{todo_id}` - Delete any todo (admin only)

### Users (`/user`)

- `GET /user/` - Get current user info
- `POST /user/change-password` - Change password
- `PUT /user/change-phone-number` - Update phone number

### Health Check

- `GET /healthy` - Application health status

## Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Database Setup

1. Install PostgreSQL and create a database:

```sql
CREATE DATABASE TodoApplicationDatabase;
```

2. Update database connection in `database.py`:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/TodoApplicationDatabase"
```

### Application Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd TodoApp
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic bcrypt python-jose python-multipart jinja2 pytest
```

4. Run database migrations:

```bash
alembic upgrade head
```

5. Start the application:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Register a new account or login with existing credentials
3. Create, edit, and manage your todos
4. Set priorities and mark todos as complete

### API Usage

1. Register a user via `POST /auth/`
2. Login to get access token via `POST /auth/token`
3. Use the token in Authorization header: `Bearer <token>`
4. Access protected endpoints

### Admin Features

- Admin users can view and delete all todos
- Admin role must be set during user creation

## Testing

Run the test suite:

```bash
pytest
```

Test files are located in the `test/` directory and cover:

- Authentication functionality
- Todo CRUD operations
- Admin operations
- User management
- Main application routes

## Security Features

- **Password Security**: Bcrypt hashing with salt
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access**: Admin and user role separation
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## Configuration

### Environment Variables

Consider setting these environment variables for production:

- `SECRET_KEY`: JWT signing secret (currently hardcoded)
- `DATABASE_URL`: Database connection string
- `ALGORITHM`: JWT algorithm (default: HS256)

### Database Migration

To create new migrations after model changes:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Development

### Adding New Features

1. Create new routes in appropriate router files
2. Update models if database changes are needed
3. Create database migrations with Alembic
4. Add corresponding templates for web interface
5. Write tests for new functionality

### Code Structure

- Follow FastAPI best practices
- Use dependency injection for database and authentication
- Separate concerns with router modules
- Maintain consistent error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
