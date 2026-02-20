import api from './api';

// Agent API service for natural language task management
const agentApi = {
  /**
   * Execute a natural language instruction through the AI Agent
   * @param {string} instruction - Natural language instruction
   * @returns {Promise<{success: boolean, response: string, error: string|null}>}
   */
  executeInstruction: async (instruction) => {
    return await api.post('/api/v1/agent/execute', { instruction });
  },

  /**
   * Check the health of the agent service
   * @returns {Promise<{status: string, service: string}>}
   */
  healthCheck: async () => {
    return await api.get('/api/v1/agent/health');
  }
};

export default agentApi;
