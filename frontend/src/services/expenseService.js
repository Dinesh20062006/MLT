import apiClient from './api';

export const expenseService = {
  async getExpenses(params = {}) {
    const response = await apiClient.get('/expenses', { params });
    return response.data;
  },

  async getExpense(id) {
    const response = await apiClient.get(`/expenses/${id}`);
    return response.data;
  },

  async createExpense(expenseData) {
    const response = await apiClient.post('/expenses', expenseData);
    return response.data;
  },

  async updateExpense(id, expenseData) {
    const response = await apiClient.put(`/expenses/${id}`, expenseData);
    return response.data;
  },

  async deleteExpense(id) {
    const response = await apiClient.delete(`/expenses/${id}`);
    return response.data;
  },

  async getCategories() {
    const response = await apiClient.get('/categories');
    return response.data;
  }
};
