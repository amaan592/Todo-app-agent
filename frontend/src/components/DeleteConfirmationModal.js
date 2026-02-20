import React from 'react';

const DeleteConfirmationModal = ({ isOpen, taskTitle, onConfirm, onCancel }) => {
  if (!isOpen) return null;

  return (
    <div className='modal-overlay'>
      <div className='modal-content'>
        <h3>Delete Task</h3>
        <p>Are you sure you want to delete the task "{taskTitle}"?</p>
        <p>This action cannot be undone.</p>
        <div className='modal-actions'>
          <button onClick={onConfirm} className='confirm-delete-btn'>
            Yes, Delete
          </button>
          <button onClick={onCancel} className='cancel-delete-btn'>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmationModal;