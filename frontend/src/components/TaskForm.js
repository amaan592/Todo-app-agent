import React, { useState } from 'react';
import taskApi from '../services/taskApi';

const TaskForm = ({ onTaskCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const newTask = {
        title: title.trim(),
        description: description.trim() || undefined,
        status: 'PENDING'
      };

      const createdTask = await taskApi.createTask(newTask);
      setTitle('');
      setDescription('');
      setError('');

      if (onTaskCreated) {
        onTaskCreated(createdTask);
      }
    } catch (err) {
      setError(err.message || 'Failed to create task');
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='task-form-container' role='region' aria-labelledby='form-heading'>
      <h2 id='form-heading'>Create New Task</h2>
      <form onSubmit={handleSubmit} className='task-form' aria-describedby={error ? 'form-error' : undefined}>
        <div className='form-group'>
          <label htmlFor='title'>Title *</label>
          <input
            type='text'
            id='title'
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder='Enter task title'
            disabled={loading}
            required
            aria-required='true'
            aria-invalid={!!error}
          />
        </div>

        <div className='form-group'>
          <label htmlFor='description'>Description</label>
          <textarea
            id='description'
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder='Enter task description (optional)'
            disabled={loading}
            rows='3'
            aria-describedby={error ? 'form-error' : undefined}
          />
        </div>

        {error && (
          <div id='form-error' className='error-message' role='alert'>
            {error}
          </div>
        )}

        <button
          type='submit'
          disabled={loading}
          className='submit-button'
          aria-busy={loading}
        >
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
};

export default TaskForm;