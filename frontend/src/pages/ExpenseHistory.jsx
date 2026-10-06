import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  Trash2, 
  Calendar, 
  ChevronLeft, 
  ChevronRight, 
  AlertCircle,
  Plus
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { expenseService } from '../services/expenseService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { EmptyState } from '../components/EmptyState';
import { formatCurrency, formatDate } from '../utils/formatters';

export const ExpenseHistory = () => {
  const [expenses, setExpenses] = useState([]);
  const [categories, setCategories] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(12);

  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [sortBy, setSortBy] = useState('expense_date');
  const [sortOrder, setSortOrder] = useState('desc');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  const fetchExpenses = async () => {
    setLoading(true);
    setError('');
    try {
      const params = {
        page,
        page_size: pageSize,
        sort_by: sortBy,
        sort_order: sortOrder,
      };
      if (searchTerm.trim()) params.search = searchTerm.trim();
      if (selectedCategory && selectedCategory !== 'All') params.category = selectedCategory;
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;

      const res = await expenseService.getExpenses(params);
      setExpenses(res.expenses || []);
      setTotal(res.total || 0);
      setTotalPages(res.total_pages || 1);
    } catch (err) {
      setError(err.message || 'Failed to fetch expenses.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchCats = async () => {
      try {
        const cats = await expenseService.getCategories();
        setCategories(cats);
      } catch (err) {
        console.error(err);
      }
    };
    fetchCats();
  }, []);

  useEffect(() => {
    fetchExpenses();
  }, [page, selectedCategory, sortBy, sortOrder, startDate, endDate]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    fetchExpenses();
  };

  const handleDelete = async (expenseId) => {
    if (!window.confirm('Are you sure you want to delete this expense record?')) {
      return;
    }
    setDeletingId(expenseId);
    try {
      await expenseService.deleteExpense(expenseId);
      fetchExpenses();
    } catch (err) {
      alert(err.message || 'Failed to delete expense.');
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Search and Filters Header */}
      <div className="card" style={{ padding: '18px 20px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '14px', alignItems: 'center', justifyContent: 'space-between' }}>
          {/* Search bar */}
          <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '8px', flex: '1 1 260px' }}>
            <div style={{ position: 'relative', width: '100%' }}>
              <input
                type="text"
                className="form-input"
                placeholder="Search description or merchant..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ paddingLeft: '36px' }}
              />
              <Search size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
            </div>
            <button type="submit" className="btn btn-secondary">
              Search
            </button>
          </form>

          {/* Filter dropdowns */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center' }}>
            {/* Category */}
            <select
              className="form-select"
              value={selectedCategory}
              onChange={(e) => { setSelectedCategory(e.target.value); setPage(1); }}
              style={{ width: 'auto', minWidth: '130px' }}
            >
              <option value="All">All Categories</option>
              {categories.map((c) => (
                <option key={c.category_id} value={c.name}>{c.name}</option>
              ))}
            </select>

            {/* Sort by */}
            <select
              className="form-select"
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [sb, so] = e.target.value.split('-');
                setSortBy(sb);
                setSortOrder(so);
                setPage(1);
              }}
              style={{ width: 'auto' }}
            >
              <option value="expense_date-desc">Newest First</option>
              <option value="expense_date-asc">Oldest First</option>
              <option value="amount-desc">Amount: High to Low</option>
              <option value="amount-asc">Amount: Low to High</option>
            </select>

            <Link to="/add-expense" className="btn btn-primary" style={{ padding: '8px 14px' }}>
              <Plus size={16} />
              <span>Add Expense</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div style={{
          padding: '14px 18px',
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          color: '#dc2626',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Main Table / Cards view */}
      {loading ? (
        <LoadingSpinner message="Loading expense records from Oracle Database..." />
      ) : expenses.length === 0 ? (
        <EmptyState
          title="No expenses found"
          description="Try adjusting your search criteria or add a new transaction."
          actionText="Add New Expense"
          actionLink="/add-expense"
        />
      ) : (
        <div className="card" style={{ padding: 0 }}>
          {/* Desktop Table View */}
          <div className="desktop-table-wrapper" style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Merchant</th>
                  <th>Category</th>
                  <th>Payment</th>
                  <th>Prediction</th>
                  <th style={{ textAlign: 'right' }}>Amount</th>
                  <th style={{ textAlign: 'center', width: '80px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {expenses.map((exp) => (
                  <tr key={exp.expense_id}>
                    <td style={{ color: '#64748b', fontSize: '0.8125rem', whiteSpace: 'nowrap' }}>
                      {formatDate(exp.expense_date)}
                    </td>
                    <td style={{ fontWeight: 500, color: '#0f172a' }}>
                      {exp.description}
                    </td>
                    <td style={{ color: '#64748b', fontSize: '0.8125rem' }}>
                      {exp.merchant || '—'}
                    </td>
                    <td>
                      <span className="badge badge-blue">
                        {exp.category}
                      </span>
                    </td>
                    <td style={{ color: '#64748b', fontSize: '0.8125rem' }}>
                      {exp.payment_method || 'UPI'}
                    </td>
                    <td>
                      {exp.predicted_category ? (
                        <span className="badge badge-green" style={{ fontSize: '0.7rem' }}>
                          AI: {exp.predicted_category}
                        </span>
                      ) : (
                        <span style={{ color: '#94a3b8', fontSize: '0.75rem' }}>—</span>
                      )}
                    </td>
                    <td style={{ textAlign: 'right', fontWeight: 600, color: '#dc2626' }}>
                      {formatCurrency(exp.amount)}
                    </td>
                    <td style={{ textAlign: 'center' }}>
                      <button
                        onClick={() => handleDelete(exp.expense_id)}
                        disabled={deletingId === exp.expense_id}
                        style={{
                          background: 'none',
                          border: 'none',
                          color: '#dc2626',
                          cursor: 'pointer',
                          padding: '6px',
                          borderRadius: '4px'
                        }}
                        title="Delete expense"
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile Card View (shown only on small screens via CSS) */}
          <div className="mobile-card-wrapper" style={{ display: 'none', padding: '16px', flexDirection: 'column', gap: '12px' }}>
            {expenses.map((exp) => (
              <div
                key={exp.expense_id}
                style={{
                  border: '1px solid #e2e8f0',
                  borderRadius: '10px',
                  padding: '14px',
                  backgroundColor: '#ffffff'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                  <div>
                    <div style={{ fontWeight: 600, color: '#0f172a', fontSize: '0.9375rem' }}>
                      {exp.description}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                      {formatDate(exp.expense_date)} {exp.merchant ? `• ${exp.merchant}` : ''}
                    </div>
                  </div>
                  <div className="financial-value" style={{ color: '#dc2626', fontSize: '1.1rem' }}>
                    {formatCurrency(exp.amount)}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #f1f5f9' }}>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <span className="badge badge-blue">
                      {exp.category}
                    </span>
                    {exp.predicted_category && (
                      <span className="badge badge-green">
                        AI: {exp.predicted_category}
                      </span>
                    )}
                  </div>

                  <button
                    onClick={() => handleDelete(exp.expense_id)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#dc2626',
                      cursor: 'pointer',
                      padding: '4px'
                    }}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination bar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '14px 20px',
            borderTop: '1px solid #e2e8f0',
            backgroundColor: '#fafbfd',
            flexWrap: 'wrap',
            gap: '10px'
          }}>
            <div style={{ fontSize: '0.8125rem', color: '#64748b' }}>
              Showing {expenses.length} of {total} transactions (Page {page} of {totalPages})
            </div>

            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-secondary"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                style={{ padding: '6px 12px', fontSize: '0.8125rem' }}
              >
                <ChevronLeft size={16} />
                <span>Previous</span>
              </button>

              <button
                className="btn btn-secondary"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                style={{ padding: '6px 12px', fontSize: '0.8125rem' }}
              >
                <span>Next</span>
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        </div>
      )}

      <style>{`
        @media (max-width: 768px) {
          .desktop-table-wrapper {
            display: none !important;
          }
          .mobile-card-wrapper {
            display: flex !important;
          }
        }
      `}</style>
    </div>
  );
};
