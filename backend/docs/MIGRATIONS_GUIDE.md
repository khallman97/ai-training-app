# 🗄️ Database Migrations Guide

## ✅ Quick Answer: No More Quick Fixes!

**From now on, Alembic will handle ALL database schema changes automatically.** The quick fix files were just temporary solutions to get you up and running.

## 🚀 Proper Migration Workflow

### **When You Make Model Changes:**

1. **Update your models** in `app/models/`
2. **Create migration:** `python scripts/docker_migrate.py migrate "Description"`
3. **Apply migration:** `python scripts/docker_migrate.py upgrade`
4. **Restart app:** `docker-compose restart backend`

### **That's it!** No more manual SQL or quick fixes needed.

## 📋 Available Commands

### **From Host Machine (Recommended):**
```bash
# Initialize database with current models
python scripts/docker_migrate.py init

# Create new migration from model changes
python scripts/docker_migrate.py migrate "Add new user fields"

# Apply pending migrations
python scripts/docker_migrate.py upgrade

# Check migration status
python scripts/docker_migrate.py status

# Rollback last migration
python scripts/docker_migrate.py downgrade

# Open shell in container
python scripts/docker_migrate.py shell
```

### **From Inside Container:**
```bash
# Open shell in container
python scripts/docker_migrate.py shell

# Then run commands inside the container
python scripts/manage_migrations.py init
python scripts/manage_migrations.py migrate "Add new fields"
python scripts/manage_migrations.py upgrade
```

## 🔄 Automatic Migration on Startup

Your Docker setup automatically:
1. **Waits for database** to be ready
2. **Runs pending migrations** before starting the app
3. **Starts the FastAPI server**

This means your app will always have the latest schema when it starts!

## 📝 Example: Adding New Fields

### **Step 1: Update Your Model**
```python
# app/models/training_plans.py
class TrainingPlan(Base):
    # ... existing fields ...
    new_field = Column(String, nullable=True)  # Add this line
```

### **Step 2: Create Migration**
```bash
python scripts/docker_migrate.py migrate "Add new_field to TrainingPlan"
```

### **Step 3: Apply Migration**
```bash
python scripts/docker_migrate.py upgrade
```

### **Step 4: Restart App**
```bash
docker-compose restart backend
```

## 🧹 Cleanup

To remove the old quick fix files:
```bash
python cleanup_quick_fixes.py
```

## ✅ Benefits of Proper Migrations

- ✅ **Version Control**: All schema changes tracked
- ✅ **Rollback**: Can undo changes if needed
- ✅ **Team Collaboration**: Everyone gets the same schema
- ✅ **Production Safe**: Tested migration process
- ✅ **Automatic**: Runs on every container start
- ✅ **No Manual SQL**: All changes handled automatically

## 🔒 Production Considerations

### **Backup Before Migrations**
```bash
# Backup your database
docker-compose exec db pg_dump -U aiuser ai_training_app > backup.sql
```

### **Test Migrations First**
Always test migrations in development before production:
```bash
python scripts/docker_migrate.py status
```

### **Rollback Plan**
If something goes wrong:
```bash
python scripts/docker_migrate.py downgrade
```

## 🎯 Summary

**Before (Quick Fixes):**
- Manual SQL scripts
- One-time fixes
- No version control
- Error-prone

**Now (Proper Migrations):**
- Automatic schema detection
- Version controlled changes
- Safe rollbacks
- Team-friendly
- Production-ready

## 🚀 Next Steps

1. **Clean up quick fixes:**
   ```bash
   python cleanup_quick_fixes.py
   ```

2. **Initialize migrations:**
   ```bash
   python scripts/docker_migrate.py init
   ```

3. **From now on, use migrations for ALL schema changes!**

Your database management is now professional-grade! 🎉 