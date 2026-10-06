import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  TrendingUp, 
  TrendingDown, 
  PiggyBank, 
  Percent, 
  Plus, 
  ArrowRight, 
  Calendar, 
  Wallet,
  AlertCircle
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell, 
  Tooltip, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Legend 
} from 'recharts';
import { analyticsService } from '../services/analyticsService';
import { expenseService } from '../services/expenseService';
import { MetricCard } from '../components/MetricCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { EmptyState } from '../components/EmptyState';
import { formatCurrency, formatDate } from '../utils/formatters';

export const Dashboard = () => {
  const [data, setData] = useState(null);
  const [recentExpenses, setRecentExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadDashboardData = async () => {
    setLoading(true);
    setError('');
    try {
      const [analyticsRes, expensesRes] = await Promise.all([
        analyticsService.getDashboardAnalytics(),
        expenseService.getExpenses({ page: 1, page_size: 5, sort_by: 'expense_date', sort_order: 'desc' })
      ]);
      setData(analyticsRes);
      setRecentExpenses(expensesRes.expenses || []);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Calculating financial metrics and loading trends..." />;
  }

  if (error) {
    return (
      <div className="card" style={{ padding: '24px', borderColor: '#fecaca', backgroundColor: '#fef2f2' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#dc2626' }}>
          <AlertCircle size={20} />
          <span style={{ fontWeight: 600 }}>{error}</span>
        </div>
        <button onClick={loadDashboardData} className="btn btn-secondary" style={{ marginTop: '16px' }}>
          Retry
        </button>
      </div>
    );
  }

  const overview = data?.overview || {};
  const categoryDistribution = data?.category_distribution || [];
  const monthlyTrend = data?.monthly_trend || [];
  const hasExpenses = (overview.total_transaction_count || 0) > 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Salary configuration notice if not set */}
      {!data?.has_salary_configured && (
        <div style={{
          backgroundColor: '#fffbeb',
          border: '1px solid #fde68a',
          borderRadius: '10px',
          padding: '14px 18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Wallet size={18} color="#d97706" />
            <span style={{ fontSize: '0.875rem', color: '#92400e', fontWeight: 500 }}>
              Set your monthly salary to view automated savings calculations and weekly estimates.
            </span>
          </div>
          <Link to="/settings" className="btn btn-secondary" style={{ fontSize: '0.8125rem', padding: '6px 12px' }}>
            Configure Salary
          </Link>
        </div>
      )}

      {/* 4 Primary Financial Cards */}
      <div className="grid-4">
        <MetricCard
          title="Monthly Income"
          value={formatCurrency(overview.monthly_income)}
          subtitle="Fixed monthly salary"
          icon={TrendingUp}
          colorScheme="blue"
          badge={{ text: 'Salary', type: 'blue' }}
        />

        <MetricCard
          title="Monthly Expenses"
          value={formatCurrency(overview.monthly_expenses)}
          subtitle="Active period total"
          icon={TrendingDown}
          colorScheme="red"
          badge={{ text: 'Expenses', type: 'red' }}
        />

        <MetricCard
          title="Monthly Savings"
          value={formatCurrency(overview.monthly_savings)}
          subtitle="Income minus expenses"
          icon={PiggyBank}
          colorScheme={overview.monthly_savings >= 0 ? 'green' : 'red'}
          badge={{ text: overview.monthly_savings >= 0 ? 'Surplus' : 'Deficit', type: overview.monthly_savings >= 0 ? 'green' : 'red' }}
        />

        <MetricCard
          title="Savings Rate"
          value={`${overview.savings_rate || 0}%`}
          subtitle="Of total monthly income"
          icon={Percent}
          colorScheme={overview.savings_rate >= 20 ? 'green' : 'amber'}
          badge={{ text: overview.savings_rate >= 50 ? 'Excellent' : 'Moderate', type: overview.savings_rate >= 50 ? 'green' : 'gray' }}
        />
      </div>

      {/* Estimated Weekly Section */}
      <div className="card" style={{ backgroundColor: '#ffffff' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: '#0f172a' }}>
              Estimated Weekly Calculations
            </div>
            <div style={{ fontSize: '0.8125rem', color: '#64748b' }}>
              Standardized weekly estimates computed via Annual Figures ÷ 52 weeks
            </div>
          </div>
          <span className="badge badge-gray" style={{ fontSize: '0.75rem' }}>
            Formula: Annual / 52
          </span>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          padding: '16px',
          backgroundColor: '#f8fafc',
          borderRadius: '8px',
          border: '1px solid #f1f5f9'
        }}>
          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 500, textTransform: 'uppercase' }}>
              Est. Weekly Income
            </div>
            <div className="financial-value" style={{ fontSize: '1.25rem', color: '#0f172a', marginTop: '4px' }}>
              {formatCurrency(overview.estimated_weekly_income)}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 500, textTransform: 'uppercase' }}>
              Est. Weekly Expenses
            </div>
            <div className="financial-value" style={{ fontSize: '1.25rem', color: '#dc2626', marginTop: '4px' }}>
              {formatCurrency(overview.estimated_weekly_expenses)}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 500, textTransform: 'uppercase' }}>
              Est. Weekly Savings
            </div>
            <div className="financial-value" style={{ fontSize: '1.25rem', color: overview.estimated_weekly_savings >= 0 ? '#16a34a' : '#dc2626', marginTop: '4px' }}>
              {formatCurrency(overview.estimated_weekly_savings)}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 500, textTransform: 'uppercase' }}>
              Projected Annual Income
            </div>
            <div className="financial-value" style={{ fontSize: '1.25rem', color: '#2563eb', marginTop: '4px' }}>
              {formatCurrency(overview.annual_income)}
            </div>
          </div>
        </div>
      </div>

      {/* Main Charts Section */}
      {hasExpenses ? (
        <div className="grid-2">
          {/* Chart 1: Expense Distribution */}
          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Expense Distribution</h3>
                <div className="card-subtitle">Breakdown by AI-classified categories</div>
              </div>
            </div>

            <div style={{ height: '280px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryDistribution}
                    dataKey="amount"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={95}
                    paddingAngle={3}
                  >
                    {categoryDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color_hex || '#2563eb'} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value) => [formatCurrency(value), 'Amount']}
                    contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '0.8125rem' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Category legends */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '10px' }}>
              {categoryDistribution.slice(0, 6).map((item) => (
                <div key={item.category} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: '#475569' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: item.color_hex }} />
                  <span>{item.category}: {item.percentage}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Chart 2: Income vs Expense vs Savings */}
          <div className="card">
            <div className="card-header">
              <div>
                <h3 className="card-title">Monthly Trend & Comparison</h3>
                <div className="card-subtitle">Income vs Expenses vs Savings</div>
              </div>
            </div>

            <div style={{ height: '280px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={monthlyTrend} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={{ stroke: '#e2e8f0' }} />
                  <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={{ stroke: '#e2e8f0' }} tickFormatter={(v) => `₹${v/1000}k`} />
                  <Tooltip 
                    formatter={(value) => [formatCurrency(value), '']}
                    contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '0.8125rem' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '0.75rem', paddingTop: '10px' }} />
                  <Bar dataKey="income" name="Income" fill="#2563eb" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="expenses" name="Expenses" fill="#dc2626" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="savings" name="Savings" fill="#16a34a" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      ) : (
        <EmptyState 
          title="No transactions recorded"
          description="Click Add Expense to use the Machine Learning model to categorize your first transaction."
          actionText="Add New Expense"
          actionLink="/add-expense"
        />
      )}

      {/* Recent Transactions Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Recent Transactions</h3>
            <div className="card-subtitle">Latest recorded expenses</div>
          </div>
          <Link to="/history" className="btn btn-secondary" style={{ fontSize: '0.8125rem', padding: '6px 12px' }}>
            <span>View All</span>
            <ArrowRight size={14} />
          </Link>
        </div>

        {recentExpenses.length > 0 ? (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Category</th>
                  <th>Payment</th>
                  <th style={{ textAlign: 'right' }}>Amount</th>
                </tr>
              </thead>
              <tbody>
                {recentExpenses.map((exp) => (
                  <tr key={exp.expense_id}>
                    <td style={{ color: '#64748b', fontSize: '0.8125rem', whiteSpace: 'nowrap' }}>
                      {formatDate(exp.expense_date)}
                    </td>
                    <td style={{ fontWeight: 500 }}>
                      {exp.description}
                      {exp.merchant && (
                        <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                          {exp.merchant}
                        </div>
                      )}
                    </td>
                    <td>
                      <span className="badge badge-blue">
                        {exp.category}
                      </span>
                    </td>
                    <td style={{ color: '#64748b', fontSize: '0.8125rem' }}>
                      {exp.payment_method || 'UPI'}
                    </td>
                    <td style={{ textAlign: 'right', fontWeight: 600, color: '#dc2626' }}>
                      {formatCurrency(exp.amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ padding: '24px', textAlign: 'center', color: '#64748b', fontSize: '0.875rem' }}>
            No recent transactions found.
          </div>
        )}
      </div>
    </div>
  );
};
