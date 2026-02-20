import React, { useState, useCallback } from 'react';
import TaskForm from './TaskForm';
import TaskList from './TaskList';
import AgentChat from './AgentChat';
import './TaskManager.css';

const TaskManager = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleTasksChanged = useCallback(() => {
    // Trigger a refresh of the task list
    setRefreshKey(prev => prev + 1);
  }, []);

  return (
    <div className='task-manager'>
      <div className='container'>
        <TaskForm />
        <AgentChat onTasksChanged={handleTasksChanged} />
        <TaskList key={refreshKey} />
      </div>
    </div>
  );
};

export default TaskManager;
