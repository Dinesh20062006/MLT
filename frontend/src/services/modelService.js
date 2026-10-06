import apiClient from './api';

export const modelService = {
  async getModelComparison() {
    const response = await apiClient.get('/model-comparison');
    return response.data;
  }
};
