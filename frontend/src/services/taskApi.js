import api from './api';

// Task API service functions
const taskApi = {
  // Create a new task
  createTask: async (taskData) => {
    return await api.post('/api/v1/tasks', taskData);
  },

  // Get all tasks
  getAllTasks: async () => {
    return await api.get('/api/v1/tasks');
  },

  // Get a specific task by ID
  getTaskById: async (taskId) => {
    return await api.get(`/api/v1/tasks/${taskId}`);
  },

  // Update a task
  updateTask: async (taskId, taskData) => {
    return await api.put(`/api/v1/tasks/${taskId}`, taskData);
  },

  // Delete a task
  deleteTask: async (taskId) => {
    return await api.delete(`/api/v1/tasks/${taskId}`);
  }
};

export default taskApi;