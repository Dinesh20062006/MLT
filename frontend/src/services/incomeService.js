import apiClient from './api';

export const incomeService = {
  async getIncome() {
    const response = await apiClient.get('/income');
    return response.data;
  },

  async updateIncome(monthlyIncome) {
    const response = await apiClient.post('/income', { monthly_income: Number(monthlyIncome) });
    return response.data;
  }
};
