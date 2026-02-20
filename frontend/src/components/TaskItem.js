import React, { useState } from 'react';
import taskApi from '../services/taskApi';
import DeleteConfirmationModal from './DeleteConfirmationModal';

const TaskItem = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStatusToggle = async () => {
    setLoading(true);
    try {
      const updatedStatus = task.status === 'PENDING' ? 'COMPLETED' : 'PENDING';
      const updatedTask = await taskApi.updateTask(task.id, {
        status: updatedStatus
      });

      if (onTaskUpdated) {
        onTaskUpdated(updatedTask);
      }
    } catch (err) {
      setError(err.message || 'Failed to update task status');
      console.error('Error updating task status:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async () => {
    setLoading(true);
    setError('');

    try {
      const updatedTask = await taskApi.updateTask(task.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined
      });

      if (onTaskUpdated) {
        onTaskUpdated(updatedTask);
      }
      setIsEditing(false);
    } catch (err) {
      setError(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      await taskApi.deleteTask(task.id);

      if (onTaskDeleted) {
        onTaskDeleted(task.id);
      }
    } catch (err) {
      setError(err.message || 'Failed to delete task');
      console.error('Error deleting task:', err);
    } finally {
      setLoading(false);
      setShowDeleteModal(false);
    }
  };

  const openDeleteModal = () => {
    setShowDeleteModal(true);
  };

  const closeDeleteModal = () => {
    setShowDeleteModal(false);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className={`task-item ${task.status.toLowerCase()}`} role='article' aria-labelledby={`task-title-${task.id}`}>
      {isEditing ? (
        <div className='task-edit-form'>
          <div className='form-group'>
            <input
              type='text'
              id={`edit-title-${task.id}`}
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              placeholder='Task title'
              disabled={loading}
              className='edit-title-input'
              aria-label={`Edit title for task ${task.title}`}
            />
          </div>

          <div className='form-group'>
            <textarea
              id={`edit-description-${task.id}`}
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              placeholder='Task description'
              disabled={loading}
              rows='2'
              className='edit-description-input'
              aria-label={`Edit description for task ${task.title}`}
            />
          </div>

          {error && (
            <div className='error-message' role='alert'>
              {error}
            </div>
          )}

          <div className='edit-actions'>
            <button
              onClick={handleEdit}
              disabled={loading}
              className='save-button'
              aria-label={`Save changes to task ${task.title}`}
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setEditTitle(task.title);
                setEditDescription(task.description || '');
                setError('');
              }}
              disabled={loading}
              className='cancel-button'
              aria-label={`Cancel editing task ${task.title}`}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className='task-header'>
            <div className='task-title'>
              <h3 id={`task-title-${task.id}`}>
                <strong>{task.title}</strong>
              </h3>
            </div>
            <div className='task-status' aria-label={`Status: ${task.status}`}>
              <span className={`status-badge ${task.status.toLowerCase()}`}>
                {task.status}
              </span>
            </div>
          </div>

          {task.description && (
            <div className='task-description' id={`task-desc-${task.id}`}>
              {task.description}
            </div>
          )}

          <div className='task-meta' aria-label={`Created: ${formatDate(task.created_at)}`}>
            <small>Created: {formatDate(task.created_at)}</small>
          </div>

          <div className='task-actions'>
            <button
              onClick={handleStatusToggle}
              disabled={loading}
              className={`status-toggle ${task.status === 'PENDING' ? 'mark-complete' : 'mark-pending'}`}
              aria-label={`${task.status === 'PENDING' ? 'Mark complete' : 'Mark pending'} for task ${task.title}`}
            >
              {task.status === 'PENDING' ? 'Mark Complete' : 'Mark Pending'}
            </button>

            <button
              onClick={() => setIsEditing(true)}
              disabled={loading}
              className='edit-button'
              aria-label={`Edit task ${task.title}`}
            >
              Edit
            </button>

            <button
              onClick={openDeleteModal}
              disabled={loading}
              className='delete-button'
              aria-label={`Delete task ${task.title}`}
            >
              Delete
            </button>
          </div>

          {error && (
            <div className='error-message' role='alert'>
              {error}
            </div>
          )}
        </>
      )}

      <DeleteConfirmationModal
        isOpen={showDeleteModal}
        taskTitle={task.title}
        onConfirm={handleDelete}
        onCancel={closeDeleteModal}
      />
    </div>
  );
};

export default TaskItem;