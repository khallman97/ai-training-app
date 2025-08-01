# 🐳 Docker Database Migrations Guide

This guide explains how to use database migrations with your Docker setup.

## 🚀 Quick Start

### 1. Start Your Docker Environment
```bash
docker-compose up -d
```

### 2. Initialize Database (First Time Only)
```bash
python docker_migrate.py init
```

### 3. When You Make Model Changes
```bash
python docker_migrate.py migrate "Description of changes"
```

### 4. Apply Migrations
```bash
python docker_migrate.py upgrade
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize database with current models |
| `migrate "message"` | Create new migration from model changes |
| `upgrade` | Apply pending migrations to database |
| `downgrade` | Rollback the last migration |
| `status` | Show migration status and history |
| `reset` | Reset database (⚠️ deletes all data) |
| `shell` | Open shell in backend container |

## 🔄 Automatic Migration on Startup

Your Docker setup now automatically:
1. **Waits for database** to be ready
2. **Runs pending migrations** before starting the app
3. **Starts the FastAPI server**

This means your app will always have the latest schema when it starts!

## 🛠️ Manual Commands

### From Host Machine (Recommended)
```bash
# Initialize database
python docker_migrate.py init

# Create migration
python docker_migrate.py migrate "Add new user fields"

# Apply migrations
python docker_migrate.py upgrade

# Check status
python docker_migrate.py status
```

### From Inside Container
```bash
# Open shell in container
python docker_migrate.py shell

# Then run commands inside the container
python manage_migrations.py init
python manage_migrations.py migrate "Add new fields"
python manage_migrations.py upgrade
```

## 🔧 Troubleshooting

### Container Won't Start
If your container fails to start due to migration issues:

1. **Check logs:**
   ```bash
   docker-compose logs backend
   ```

2. **Reset database (if needed):**
   ```bash
   python docker_migrate.py reset
   ```

3. **Rebuild container:**
   ```bash
   docker-compose down
   docker-compose build --no-cache backend
   docker-compose up -d
   ```

### Migration Conflicts
If you get migration conflicts:

1. **Check current status:**
   ```bash
   python docker_migrate.py status
   ```

2. **Open shell and resolve manually:**
   ```bash
   python docker_migrate.py shell
   # Then inside container:
   python manage_migrations.py status
   ```

### Database Connection Issues
Make sure your database container is running:
```bash
docker-compose ps
```

If not running:
```bash
docker-compose up -d db
```

## 📝 Example Workflow

### Adding New Fields to TrainingPlan Model

1. **Update your model** in `backend/training_plans.py`:
   ```python
   class TrainingPlan(Base):
       # ... existing fields ...
       new_field = Column(String, nullable=True)
   ```

2. **Create migration:**
   ```bash
   python docker_migrate.py migrate "Add new_field to TrainingPlan"
   ```

3. **Apply migration:**
   ```bash
   python docker_migrate.py upgrade
   ```

4. **Restart your app** (migrations run automatically):
   ```bash
   docker-compose restart backend
   ```

## 🔒 Production Considerations

### Backup Before Migrations
```bash
# Backup your database
docker-compose exec db pg_dump -U aiuser ai_training_app > backup.sql
```

### Test Migrations First
Always test migrations in development before production:
```bash
# Test migration without applying
python docker_migrate.py status
```

### Rollback Plan
If something goes wrong:
```bash
python docker_migrate.py downgrade
```

## 📁 File Structure

```
backend/
├── Dockerfile              # Updated to include migrations
├── start.sh               # Startup script with migrations
├── manage_migrations.py   # Migration management (inside container)
├── docker_migrate.py      # Migration management (from host)
├── alembic.ini           # Alembic configuration
├── migrations/
│   ├── env.py            # Migration environment
│   ├── script.py.mako    # Migration template
│   └── versions/         # Generated migration files
└── MIGRATIONS_README.md  # Detailed migration docs

docker-compose.yml        # Updated to use startup script
DOCKER_MIGRATIONS.md      # This file
```

## ✅ Benefits

- ✅ **Automatic**: Migrations run on every container start
- ✅ **Safe**: Database connectivity checks before migrations
- ✅ **Versioned**: All schema changes tracked
- ✅ **Rollback**: Can undo changes if needed
- ✅ **Docker-native**: Works seamlessly with your container setup
- ✅ **No manual SQL**: All changes handled automatically

## 🎯 Next Steps

1. **Initialize your database:**
   ```bash
   python docker_migrate.py init
   ```

2. **Start your containers:**
   ```bash
   docker-compose up -d
   ```

3. **Your app will automatically have the latest schema!**

Now you can make model changes and they'll be automatically applied to your database without any manual intervention! 