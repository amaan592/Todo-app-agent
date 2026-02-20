# Todo Application

A full-stack Todo application with a React frontend and FastAPI backend, demonstrating professional client-server architecture.

## Overview

This application allows users to:
- Create, read, update, and delete tasks
- View tasks with clear status indicators (Pending/Completed)
- Filter tasks by status
- Undo task deletions

The application follows a clean separation of concerns with:
- React frontend consuming REST API
- FastAPI backend providing data services
- SQLAlchemy ORM for database interactions

## Architecture

The application follows a strict client-server architecture:
- **Frontend**: React components consuming backend APIs
- **Backend**: FastAPI providing REST endpoints
- **Database**: SQLite (default) or PostgreSQL for data persistence

All data flows through the backend API as required by the architectural constraints.

## Prerequisites

- Node.js v16+
- Python 3.9+
- pip (Python package manager)
- npm or yarn (Node.js package manager)

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # The .env file should already exist with default settings
   cat .env
   ```

4. Run the backend server:
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the frontend development server:
   ```bash
   npm start
   ```

## Running Both Servers

For development, run both servers in separate terminals:

Backend:
```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`.

## API Endpoints

- `GET /api/v1/tasks` - Get all tasks
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task

## Project Structure

```
backend/
├── src/
│   ├── api/          # API route definitions
│   ├── models/       # Database models
│   ├── services/     # Business logic
│   ├── schemas/      # Pydantic schemas
│   └── database.py   # Database configuration
├── requirements.txt  # Python dependencies
├── .env             # Environment variables
└── pyproject.toml   # Project configuration

frontend/
├── src/
│   ├── components/   # React components
│   ├── services/     # API service layer
│   └── App.js       # Main application component
├── public/          # Static assets
├── package.json     # Node.js dependencies
└── .env            # Environment variables
```

## Features

- **Task Management**: Full CRUD operations for tasks
- **Status Tracking**: Visual indicators for task status
- **Task Filtering**: Filter tasks by status (all, pending, completed)
- **Edit Functionality**: Edit task title and description
- **Delete Confirmation**: Modal confirmation before deletion
- **Undo Capability**: Undo recent deletions
- **Responsive Design**: Clean UI that works on different screen sizes
- **Error Handling**: Proper error display and validation
- **Loading States**: Visual feedback during API calls