import React from 'react';
import './App.css';
import TaskManager from './components/TaskManager';
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <div className='App'>
        <header className='App-header'>
          <h1>Todo Application</h1>
        </header>
        <main>
          <TaskManager />
        </main>
      </div>
    </ErrorBoundary>
  );
}

export default App;