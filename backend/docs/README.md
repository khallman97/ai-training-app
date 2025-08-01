# AI Training App Backend

A FastAPI-based backend for managing user authentication and training plans.

## 🏗️ Project Structure

```
backend/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   ├── auth.py        # User model
│   │   └── training_plans.py # TrainingPlan model
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   ├── auth.py        # Auth endpoints
│   │   └── training_plans.py # Training plan endpoints
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── database.py    # Database setup
│   │   └── security.py    # Security utilities
│   └── utils/             # Utility functions
│       └── __init__.py
├── migrations/            # Database migrations
├── scripts/               # Utility scripts
│   ├── quick_fix.py
│   ├── docker_migrate.py
│   └── manage_migrations.py
├── tests/                 # Test files
├── docs/                  # Documentation
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── alembic.ini
```

## 🚀 Quick Start

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
# Start the application
docker-compose up -d

# Run database fix (if needed)
python scripts/quick_fix.py
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Database Management

### Quick Fix (Recommended)
```bash
python scripts/quick_fix.py
```

### Using Migrations
```bash
# Initialize migrations
python scripts/manage_migrations.py init

# Create new migration
python scripts/manage_migrations.py migrate "Description"

# Apply migrations
python scripts/manage_migrations.py upgrade
```

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/
```

## 📝 Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (for production)

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS middleware configured
- Input validation with Pydantic

## 📦 Dependencies

- FastAPI: Web framework
- SQLAlchemy: ORM
- PostgreSQL: Database
- Alembic: Database migrations
- Pydantic: Data validation
- JWT: Authentication 