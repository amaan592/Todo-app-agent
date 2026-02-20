import React, { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import taskApi from '../services/taskApi';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'completed'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [recentlyDeleted, setRecentlyDeleted] = useState(null);
  const [undoTimeout, setUndoTimeout] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    // Apply filter whenever tasks or filter value changes
    if (tasks.length > 0) {
      switch (filter) {
        case 'pending':
          setFilteredTasks(tasks.filter(task => task.status === 'PENDING'));
          break;
        case 'completed':
          setFilteredTasks(tasks.filter(task => task.status === 'COMPLETED'));
          break;
        default: // 'all'
          setFilteredTasks(tasks);
      }
    } else {
      setFilteredTasks([]);
    }
  }, [tasks, filter]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const fetchedTasks = await taskApi.getAllTasks();
      setTasks(fetchedTasks);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks(prev => prev.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (deletedTaskId) => {
    // Store the deleted task for potential undo
    const deletedTask = tasks.find(task => task.id === deletedTaskId);
    if (deletedTask) {
      setRecentlyDeleted(deletedTask);

      // Remove the task optimistically
      setTasks(prev => prev.filter(task => task.id !== deletedTaskId));

      // Set up undo functionality
      if (undoTimeout) {
        clearTimeout(undoTimeout);
      }

      const timeout = setTimeout(() => {
        setRecentlyDeleted(null);
      }, 5000); // 5 seconds to undo

      setUndoTimeout(timeout);
    }
  };

  const handleUndoDelete = async () => {
    if (recentlyDeleted) {
      try {
        // Recreate the task via API
        const recreatedTask = await taskApi.createTask({
          title: recentlyDeleted.title,
          description: recentlyDeleted.description,
          status: recentlyDeleted.status
        });

        // Add it back to the tasks list
        setTasks(prev => [...prev, recreatedTask]);
        setRecentlyDeleted(null);

        if (undoTimeout) {
          clearTimeout(undoTimeout);
          setUndoTimeout(null);
        }
      } catch (err) {
        console.error('Error restoring task:', err);
        setError('Failed to restore task');
      }
    }
  };

  if (loading) {
    return <div className='loading'>Loading tasks...</div>;
  }

  if (error) {
    return <div className='error-message'>Error: {error}</div>;
  }

  return (
    <div className='task-list-container' role='region' aria-labelledby='task-list-heading'>
      <div className='task-list-header'>
        <h2 id='task-list-heading'>Task List ({tasks.length})</h2>
        <div className='filter-controls'>
          <label htmlFor='filter-select'>Filter:</label>
          <select
            id='filter-select'
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className='filter-select'
            aria-label='Filter tasks by status'
          >
            <option value='all'>All Tasks</option>
            <option value='pending'>Pending Only</option>
            <option value='completed'>Completed Only</option>
          </select>
        </div>
      </div>

      {recentlyDeleted && (
        <div className='undo-notification' role='status' aria-live='polite'>
          <span>Task "{recentlyDeleted.title}" deleted</span>
          <button
            onClick={handleUndoDelete}
            className='undo-button'
            aria-label={`Restore task ${recentlyDeleted.title}`}
          >
            Undo
          </button>
        </div>
      )}

      {filteredTasks.length === 0 ? (
        <div className='no-tasks' role='status'>
          {filter === 'all'
            ? 'No tasks available. Create your first task!'
            : `No ${filter} tasks available.`}
        </div>
      ) : (
        <div className='task-list' role='list' aria-label={`List of ${filter} tasks`}>
          {filteredTasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;