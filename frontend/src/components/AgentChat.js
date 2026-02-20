import React, { useState } from 'react';
import agentApi from '../services/agentApi';
import './AgentChat.css';

const AgentChat = ({ onTasksChanged }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'agent',
      content: 'Hello! I\'m your AI assistant for task management. You can tell me what to do in natural language, like:\n\n• "Add a task to buy groceries tomorrow"\n• "Show me my pending tasks"\n• "Mark task 1 as complete"\n• "Delete task 2"\n\nHow can I help you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setError('');

    // Add user message to chat
    const userMsg = {
      id: Date.now(),
      type: 'user',
      content: userMessage
    };
    setMessages(prev => [...prev, userMsg]);

    // Add loading message
    const loadingId = Date.now() + 1;
    setMessages(prev => [...prev, {
      id: loadingId,
      type: 'agent',
      content: '...',
      isLoading: true
    }]);

    setLoading(true);

    try {
      const response = await agentApi.executeInstruction(userMessage);
      
      // Remove loading message and add response
      setMessages(prev => prev.filter(m => m.id !== loadingId));
      
      const agentMsg = {
        id: Date.now() + 2,
        type: 'agent',
        content: response.response,
        success: response.success
      };
      
      setMessages(prev => [...prev, agentMsg]);

      // If the operation was successful, notify parent to refresh tasks
      if (response.success && onTasksChanged) {
        onTasksChanged();
      }
    } catch (err) {
      // Remove loading message and add error
      setMessages(prev => prev.filter(m => m.id !== loadingId));
      
      const errorMsg = {
        id: Date.now() + 2,
        type: 'agent',
        content: err.message || 'Sorry, I encountered an error. Please try again.',
        success: false
      };
      
      setMessages(prev => [...prev, errorMsg]);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'agent',
        content: 'Chat cleared! How can I help you with your tasks?'
      }
    ]);
    setError('');
  };

  return (
    <div className="agent-chat">
      <div className="agent-chat-header">
        <h3>🤖 AI Assistant</h3>
        <button 
          onClick={clearChat} 
          className="clear-chat-btn"
          aria-label="Clear chat"
        >
          Clear
        </button>
      </div>
      
      <div className="agent-chat-messages" role="log" aria-live="polite">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.type} ${message.isLoading ? 'loading' : ''} ${message.success === false ? 'error' : ''}`}
          >
            <div className="message-content">
              {message.content.split('\n').map((line, i) => (
                <React.Fragment key={i}>
                  {line}
                  {i < message.content.split('\n').length - 1 && <br />}
                </React.Fragment>
              ))}
            </div>
          </div>
        ))}
      </div>

      {error && (
        <div className="agent-error" role="alert">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="agent-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your instruction..."
          disabled={loading}
          className="agent-input"
          aria-label="Chat input"
          autoComplete="off"
        />
        <button 
          type="submit" 
          disabled={loading || !input.trim()}
          className="agent-submit-btn"
          aria-label="Send message"
        >
          {loading ? '...' : 'Send'}
        </button>
      </form>

      <div className="agent-examples">
        <span>Try:</span>
        <button onClick={() => setInput('Show me my tasks')} disabled={loading}>
          "Show me my tasks"
        </button>
        <button onClick={() => setInput('Add a task to buy groceries')} disabled={loading}>
          "Add a task..."
        </button>
        <button onClick={() => setInput('Mark task 1 complete')} disabled={loading}>
          "Mark task complete"
        </button>
      </div>
    </div>
  );
};

export default AgentChat;
