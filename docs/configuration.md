# Environment Configuration

This document describes the environment configuration for the Todo Application.

## Backend Configuration

### Environment Variables

The backend uses a `.env` file to manage environment-specific configurations:

```env
DATABASE_URL=sqlite:///./todo.db
LOG_LEVEL=INFO
```

#### Available Variables

- `DATABASE_URL`: Connection string for the database
  - For SQLite: `sqlite:///./filename.db`
  - For PostgreSQL: `postgresql://username:password@host:port/database_name`
  - For development: `sqlite:///./todo.db` (default)
  - For production: Use PostgreSQL connection string

- `LOG_LEVEL`: Logging level for the application
  - Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  - Default: `INFO`

### Running with Different Environments

To run the backend with different configurations:

```bash
# Development (default)
DATABASE_URL=sqlite:///./todo_dev.db LOG_LEVEL=DEBUG uvicorn src.main:app --reload

# Production
DATABASE_URL=postgresql://user:pass@prod-server:5432/proddb LOG_LEVEL=WARNING uvicorn src.main:app --workers 4
```

## Frontend Configuration

### Environment Variables

The frontend uses environment variables prefixed with `REACT_APP_`:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

#### Available Variables

- `REACT_APP_API_BASE_URL`: Base URL for the backend API
  - Default: `http://localhost:8000`
  - For development: `http://localhost:8000`
  - For production: Your production backend URL

### Setting Up Environment Files

#### Backend

Create a `.env` file in the `backend/` directory:

```bash
# Development environment
DATABASE_URL=sqlite:///./todo_dev.db
LOG_LEVEL=DEBUG

# Production environment
# DATABASE_URL=postgresql://username:password@host:port/database_name
# LOG_LEVEL=WARNING
```

#### Frontend

Create a `.env` file in the `frontend/` directory:

```bash
# Development environment
REACT_APP_API_BASE_URL=http://localhost:8000

# Production environment
# REACT_APP_API_BASE_URL=https://api.yourdomain.com
```

## Common Configuration Scenarios

### Development Setup

```env
# backend/.env
DATABASE_URL=sqlite:///./todo_dev.db
LOG_LEVEL=DEBUG
```

```env
# frontend/.env
REACT_APP_API_BASE_URL=http://localhost:8000
```

### Production Setup

```env
# backend/.env
DATABASE_URL=postgresql://prod_user:prod_pass@prod_db_server:5432/prod_todo_db
LOG_LEVEL=WARNING
```

```env
# frontend/.env
REACT_APP_API_BASE_URL=https://api.yourdomain.com
```

## Docker Configuration (if using containers)

When deploying with Docker, you can pass environment variables using the `-e` flag:

```bash
# For backend container
docker run -e DATABASE_URL=postgresql://... -e LOG_LEVEL=INFO todo-backend

# For frontend container
docker run -e REACT_APP_API_BASE_URL=https://api.yourdomain.com todo-frontend
```

## Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Verify that `REACT_APP_API_BASE_URL` is set correctly
   - Check that the backend server is running and accessible
   - Ensure CORS settings allow the frontend domain

2. **Database Connection Issues**
   - Verify the `DATABASE_URL` is formatted correctly
   - Ensure the database server is running and accessible
   - Check that the database exists and has proper permissions

3. **Environment Variables Not Loading**
   - Ensure environment files are named correctly (`.env`)
   - Check that files are in the correct directories
   - Restart the application after changing environment variables