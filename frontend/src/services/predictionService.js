import apiClient from './api';

export const predictionService = {
  async predictCategory(data) {
    const response = await apiClient.post('/predict', data);
    return response.data;
  }
};
