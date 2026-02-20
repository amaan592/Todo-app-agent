# Quickstart Guide: Todo Application

## Overview
This guide provides step-by-step instructions to set up, run, and test the full-stack Todo application with a React frontend and FastAPI backend.

## Prerequisites
- Node.js v16+ (for frontend development)
- Python 3.9+ (for backend development)
- pip (Python package manager)
- npm or yarn (Node.js package manager)
- Git

## Backend Setup (FastAPI)

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install backend dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```
   DATABASE_URL=sqlite:///./todo.db
   # For PostgreSQL: postgresql://username:password@localhost/dbname
   ```

5. **Run the backend server**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

   The backend will be available at `http://localhost:8000`

6. **Access API documentation**
   Visit `http://localhost:8000/docs` for interactive API documentation

## Frontend Setup (React)

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure API base URL**
   Create a `.env` file in the frontend directory:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```

4. **Run the frontend development server**
   ```bash
   npm start
   # or
   yarn start
   ```

   The frontend will be available at `http://localhost:3000`

## Running Both Servers

For development, run both servers in separate terminals:

Terminal 1 (Backend):
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```

## API Endpoints

The application uses the following API endpoints:

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Testing the Application

1. **Manual Testing**
   - Access the frontend at `http://localhost:3000`
   - Create a new task with title and description
   - Verify the task appears in the task list
   - Toggle the task status between pending and completed
   - Delete a task and verify it's removed

2. **API Testing**
   - Use the interactive documentation at `http://localhost:8000/docs`
   - Manually test each endpoint with sample data
   - Verify proper error handling with invalid inputs

## Environment Configuration

### Development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Database: SQLite file (for simplicity in development)

### Production
- Backend: `https://api.yourdomain.com`
- Frontend: `https://yourdomain.com`
- Database: PostgreSQL (recommended for production)

## Troubleshooting

### Common Issues

1. **CORS errors**: Ensure the backend CORS middleware allows the frontend origin
2. **Database connection**: Verify database URL in environment variables
3. **Port conflicts**: Change ports if 8000 (backend) or 3000 (frontend) are in use
4. **Dependency issues**: Clear node_modules and reinstall if frontend has problems

### Verification Steps

1. Check that the backend server is running and accessible
2. Verify the API endpoints return expected responses
3. Confirm the frontend can communicate with the backend
4. Test all CRUD operations work as expected

## Next Steps

1. Implement the backend API endpoints according to the OpenAPI specification
2. Build the frontend components following the design specifications
3. Connect frontend to backend API endpoints
4. Add error handling and loading states
5. Implement comprehensive testing