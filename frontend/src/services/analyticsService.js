import apiClient from './api';

export const analyticsService = {
  async getDashboardAnalytics() {
    const response = await apiClient.get('/analytics');
    return response.data;
  },

  async getWeeklyAnalytics() {
    const response = await apiClient.get('/analytics/weekly');
    return response.data;
  },

  async getMonthlyAnalytics() {
    const response = await apiClient.get('/analytics/monthly');
    return response.data;
  },

  async getAnnualAnalytics() {
    const response = await apiClient.get('/analytics/annual');
    return response.data;
  }
};
