import React, { useState, useEffect } from 'react';
import { 
  TrendingDown, 
  BarChart2, 
  ArrowUpRight, 
  Award, 
  PieChart as PieIcon, 
  Calendar,
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
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Legend 
} from 'recharts';
import { analyticsService } from '../services/analyticsService';
import { MetricCard } from '../components/MetricCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { formatCurrency, formatPercentage } from '../utils/formatters';

export const Analytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError('');
      try {
        const res = await analyticsService.getDashboardAnalytics();
        setData(res);
      } catch (err) {
        setError(err.message || 'Failed to load financial analytics.');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Aggregating financial analytics and projections..." />;
  }

  if (error) {
    return (
      <div className="card" style={{ padding: '24px', backgroundColor: '#fef2f2', borderColor: '#fecaca' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#dc2626' }}>
          <AlertCircle size={20} />
          <span style={{ fontWeight: 600 }}>{error}</span>
        </div>
      </div>
    );
  }

  const overview = data?.overview || {};
  const categoryDistribution = data?.category_distribution || [];
  const monthlyTrend = data?.monthly_trend || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* 4 Summary Stat Cards */}
      <div className="grid-4">
        <MetricCard
          title="Total Lifetime Expenses"
          value={formatCurrency(overview.total_lifetime_expenses)}
          subtitle={`${overview.total_transaction_count || 0} total transactions`}
          icon={TrendingDown}
          colorScheme="red"
        />

        <MetricCard
          title="Average Expense"
          value={formatCurrency(overview.average_expense_amount)}
          subtitle="Mean per transaction"
          icon={BarChart2}
          colorScheme="blue"
        />

        <MetricCard
          title="Highest Expense"
          value={formatCurrency(overview.highest_expense_amount)}
          subtitle="Largest single transaction"
          icon={ArrowUpRight}
          colorScheme="amber"
        />

        <MetricCard
          title="Most Used Category"
          value={overview.most_used_category || 'N/A'}
          subtitle="Highest transaction volume"
          icon={Award}
          colorScheme="green"
        />
      </div>

      {/* Projections Matrix Table (Weekly, Monthly, Annual) */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Multi-Horizon Financial Breakdown</h3>
            <div className="card-subtitle">
              Calculated across Weekly Estimates, Monthly Activity, and Annual Projections
            </div>
          </div>
          <span className="badge badge-gray">Consistent Backend Engine</span>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Horizon</th>
                <th>Income</th>
                <th>Expenses</th>
                <th>Savings</th>
                <th>Savings Rate</th>
                <th>Formula / Basis</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={{ fontWeight: 600 }}>
                  <span className="badge badge-blue">Estimated Weekly</span>
                </td>
                <td className="financial-value">{formatCurrency(overview.estimated_weekly_income)}</td>
                <td className="financial-value" style={{ color: '#dc2626' }}>{formatCurrency(overview.estimated_weekly_expenses)}</td>
                <td className="financial-value" style={{ color: overview.estimated_weekly_savings >= 0 ? '#16a34a' : '#dc2626' }}>
                  {formatCurrency(overview.estimated_weekly_savings)}
                </td>
                <td>{overview.savings_rate || 0}%</td>
                <td style={{ color: '#64748b', fontSize: '0.8125rem' }}>Annual ÷ 52 weeks</td>
              </tr>

              <tr>
                <td style={{ fontWeight: 600 }}>
                  <span className="badge badge-gray">Monthly</span>
                </td>
                <td className="financial-value">{formatCurrency(overview.monthly_income)}</td>
                <td className="financial-value" style={{ color: '#dc2626' }}>{formatCurrency(overview.monthly_expenses)}</td>
                <td className="financial-value" style={{ color: overview.monthly_savings >= 0 ? '#16a34a' : '#dc2626' }}>
                  {formatCurrency(overview.monthly_savings)}
                </td>
                <td>
                  <span className={`badge ${overview.savings_rate >= 20 ? 'badge-green' : 'badge-gray'}`}>
                    {overview.savings_rate || 0}%
                  </span>
                </td>
                <td style={{ color: '#64748b', fontSize: '0.8125rem' }}>Salary - Monthly Expenses</td>
              </tr>

              <tr>
                <td style={{ fontWeight: 600 }}>
                  <span className="badge badge-gray">Annual</span>
                </td>
                <td className="financial-value">{formatCurrency(overview.annual_income)}</td>
                <td className="financial-value" style={{ color: '#dc2626' }}>{formatCurrency(overview.annual_expenses)}</td>
                <td className="financial-value" style={{ color: overview.annual_savings >= 0 ? '#16a34a' : '#dc2626' }}>
                  {formatCurrency(overview.annual_savings)}
                </td>
                <td>{overview.savings_rate || 0}%</td>
                <td style={{ color: '#64748b', fontSize: '0.8125rem' }}>Monthly × 12</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Category-wise Expenses Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Category-Wise Expenses</h3>
            <div className="card-subtitle">Aggregate expenditure grouped by predicted and confirmed category</div>
          </div>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Transactions</th>
                <th>Percentage of Spend</th>
                <th style={{ textAlign: 'right' }}>Total Expenditure</th>
              </tr>
            </thead>
            <tbody>
              {categoryDistribution.map((item) => (
                <tr key={item.category}>
                  <td style={{ fontWeight: 500 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: item.color_hex }} />
                      <span>{item.category}</span>
                    </div>
                  </td>
                  <td style={{ color: '#64748b' }}>{item.count} items</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <div style={{ flex: 1, maxWidth: '120px', height: '6px', backgroundColor: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
                        <div style={{ width: `${item.percentage}%`, height: '100%', backgroundColor: item.color_hex }} />
                      </div>
                      <span style={{ fontSize: '0.8125rem', color: '#64748b' }}>{item.percentage}%</span>
                    </div>
                  </td>
                  <td style={{ textAlign: 'right', fontWeight: 600, color: '#0f172a' }}>
                    {formatCurrency(item.amount)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid-2">
        {/* Chart 1: Category Expense Distribution */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">1. Category Expense Distribution</h3>
              <div className="card-subtitle">Proportional share of total expenses</div>
            </div>
          </div>
          <div style={{ height: '260px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryDistribution}
                  dataKey="amount"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={85}
                  innerRadius={50}
                  paddingAngle={3}
                >
                  {categoryDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color_hex || '#2563eb'} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [formatCurrency(value), 'Spend']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Monthly Expense Trend */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">2. Monthly Expense Trend</h3>
              <div className="card-subtitle">Historical month-by-month spending curve</div>
            </div>
          </div>
          <div style={{ height: '260px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyTrend} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(v) => `₹${v/1000}k`} />
                <Tooltip formatter={(value) => [formatCurrency(value), 'Expenses']} />
                <Line type="monotone" dataKey="expenses" stroke="#dc2626" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Income vs Expenses */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">3. Income vs Expenses</h3>
              <div className="card-subtitle">Comparative earnings vs outflow</div>
            </div>
          </div>
          <div style={{ height: '260px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyTrend} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(v) => `₹${v/1000}k`} />
                <Tooltip formatter={(value) => [formatCurrency(value), '']} />
                <Legend wrapperStyle={{ fontSize: '0.75rem' }} />
                <Bar dataKey="income" name="Income" fill="#2563eb" radius={[4, 4, 0, 0]} />
                <Bar dataKey="expenses" name="Expenses" fill="#dc2626" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Savings Trend */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="card-title">4. Savings Trend</h3>
              <div className="card-subtitle">Net accumulated surplus progression</div>
            </div>
          </div>
          <div style={{ height: '260px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyTrend} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748b' }} tickFormatter={(v) => `₹${v/1000}k`} />
                <Tooltip formatter={(value) => [formatCurrency(value), 'Savings']} />
                <Line type="monotone" dataKey="savings" stroke="#16a34a" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
