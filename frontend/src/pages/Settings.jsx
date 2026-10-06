import React, { useState, useEffect } from 'react';
import { 
  Wallet, 
  User, 
  Moon, 
  Sun, 
  CheckCircle2, 
  AlertCircle,
  Save
} from 'lucide-react';
import { incomeService } from '../services/incomeService';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { formatCurrency } from '../utils/formatters';

export const Settings = () => {
  const { user } = useAuth();
  const [monthlyIncome, setMonthlyIncome] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  // Theme preference
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const fetchIncome = async () => {
      setLoading(true);
      setError('');
      try {
        const res = await incomeService.getIncome();
        setMonthlyIncome(res.monthly_income ? res.monthly_income.toString() : '50000');
      } catch (err) {
        setError(err.message || 'Failed to load income settings.');
      } finally {
        setLoading(false);
      }
    };
    fetchIncome();
  }, []);

  const handleSaveIncome = async (e) => {
    e.preventDefault();
    setSuccess('');
    setError('');

    const val = parseFloat(monthlyIncome);
    if (isNaN(val) || val < 0) {
      setError('Please enter a valid monthly salary (0 or higher).');
      return;
    }

    setSaving(true);
    try {
      await incomeService.updateIncome(val);
      setSuccess('Monthly salary saved successfully to Oracle Database!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update salary.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading user configuration..." />;
  }

  return (
    <div style={{ maxWidth: '720px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Notifications */}
      {error && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 16px',
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          color: '#dc2626',
          fontSize: '0.875rem'
        }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '12px 16px',
          backgroundColor: '#f0fdf4',
          border: '1px solid #bbf7d0',
          borderRadius: '8px',
          color: '#16a34a',
          fontSize: '0.875rem'
        }}>
          <CheckCircle2 size={18} />
          <span>{success}</span>
        </div>
      )}

      {/* Monthly Salary Configuration Section */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Monthly Income Configuration</h2>
            <div className="card-subtitle">
              Enter your baseline monthly earnings for financial savings analytics
            </div>
          </div>
          <Wallet size={20} color="#2563eb" />
        </div>

        <form onSubmit={handleSaveIncome}>
          <div className="form-group">
            <label className="form-label" htmlFor="settings-income">
              Monthly Salary (₹ INR)
            </label>
            <div style={{ display: 'flex', gap: '12px' }}>
              <input
                id="settings-income"
                type="number"
                min="0"
                step="any"
                className="form-input"
                value={monthlyIncome}
                onChange={(e) => setMonthlyIncome(e.target.value)}
                placeholder="50000"
                required
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={saving}
                style={{ padding: '0 24px', whiteSpace: 'nowrap' }}
              >
                <Save size={16} />
                <span>{saving ? 'Saving...' : 'Save Income'}</span>
              </button>
            </div>
          </div>

          <div style={{
            padding: '12px 16px',
            backgroundColor: '#f8fafc',
            borderRadius: '8px',
            fontSize: '0.8125rem',
            color: '#64748b'
          }}>
            <strong>Automatic Analytics Calculation:</strong> Setting your income enables real-time
            Monthly Savings, Annual Projections (12x), and Estimated Weekly (Annual ÷ 52) analytics.
          </div>
        </form>
      </div>

      {/* User Profile Section */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">User Profile</h2>
            <div className="card-subtitle">Account information associated with current session</div>
          </div>
          <User size={20} color="#64748b" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
              Full Name
            </div>
            <div style={{ fontSize: '1rem', fontWeight: 500, color: '#0f172a', marginTop: '4px' }}>
              {user?.full_name || 'Demo User'}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
              Email Address
            </div>
            <div style={{ fontSize: '1rem', fontWeight: 500, color: '#0f172a', marginTop: '4px' }}>
              {user?.email || 'demo@smartexpense.com'}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
              Database Record
            </div>
            <div style={{ fontSize: '0.875rem', color: '#2563eb', fontWeight: 500, marginTop: '4px' }}>
              Oracle DB XE • User ID {user?.user_id || 1}
            </div>
          </div>
        </div>
      </div>

      {/* Theme Toggle Section */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Application Theme</h2>
            <div className="card-subtitle">Select visual appearance mode (Default: Light Mode)</div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            type="button"
            onClick={() => setTheme('light')}
            className={`btn ${theme === 'light' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ flex: 1, padding: '12px' }}
          >
            <Sun size={16} />
            <span>Light Mode (Active Default)</span>
          </button>

          <button
            type="button"
            onClick={() => setTheme('dark')}
            className={`btn ${theme === 'dark' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ flex: 1, padding: '12px' }}
          >
            <Moon size={16} />
            <span>Dark Mode</span>
          </button>
        </div>
      </div>
    </div>
  );
};
