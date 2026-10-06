import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  RotateCcw,
  Tag,
  CreditCard,
  Building,
  Calendar,
  IndianRupee
} from 'lucide-react';
import { predictionService } from '../services/predictionService';
import { expenseService } from '../services/expenseService';
import { formatCurrency } from '../utils/formatters';

const PAYMENT_METHODS = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Cash'];

export const AddExpense = () => {
  const navigate = useNavigate();

  // Form State
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [expenseDate, setExpenseDate] = useState(new Date().toISOString().split('T')[0]);
  const [paymentMethod, setPaymentMethod] = useState('UPI');
  const [merchant, setMerchant] = useState('');

  // Categories list
  const [categories, setCategories] = useState([]);

  // Prediction State
  const [predicting, setPredicting] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('');

  // Saving State
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchCats = async () => {
      try {
        const cats = await expenseService.getCategories();
        setCategories(cats);
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    };
    fetchCats();
  }, []);

  // Quick preset helper for easy academic demonstration
  const handleQuickPreset = (descText, amtVal, merchVal, pmVal) => {
    setDescription(descText);
    setAmount(amtVal.toString());
    setMerchant(merchVal);
    setPaymentMethod(pmVal);
    setPredictionResult(null);
    setError('');
  };

  const handlePredict = async (e) => {
    if (e) e.preventDefault();
    setError('');
    setSuccess('');

    if (!description.trim()) {
      setError('Please enter an expense description.');
      return;
    }
    const numAmount = parseFloat(amount);
    if (isNaN(numAmount) || numAmount <= 0) {
      setError('Please enter a valid expense amount greater than zero.');
      return;
    }

    setPredicting(true);
    try {
      const res = await predictionService.predictCategory({
        description: description.trim(),
        amount: numAmount,
        merchant: merchant.trim() || undefined,
        payment_method: paymentMethod,
        transaction_date: expenseDate
      });

      setPredictionResult(res);
      setSelectedCategory(res.category);
    } catch (err) {
      setError(err.message || 'Error occurred while contacting prediction engine.');
    } finally {
      setPredicting(false);
    }
  };

  const handleConfirmAndSave = async () => {
    setError('');
    const numAmount = parseFloat(amount);
    if (!description.trim() || isNaN(numAmount) || numAmount <= 0 || !selectedCategory) {
      setError('Please verify all expense details before saving.');
      return;
    }

    setSaving(true);
    try {
      await expenseService.createExpense({
        description: description.trim(),
        amount: numAmount,
        category: selectedCategory,
        predicted_category: predictionResult?.category || selectedCategory,
        merchant: merchant.trim() || undefined,
        payment_method: paymentMethod,
        expense_date: expenseDate
      });

      setSuccess('Expense logged successfully to Oracle Database!');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1200);
    } catch (err) {
      setError(err.message || 'Failed to save expense.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ maxWidth: '820px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Demonstration quick test chips */}
      <div className="card" style={{ padding: '16px 20px', backgroundColor: '#f8fafc' }}>
        <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#475569', marginBottom: '8px' }}>
          Quick Demo Presets (from Project Specification):
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          <button
            type="button"
            onClick={() => handleQuickPreset('Swiggy dinner', 350, 'Swiggy', 'UPI')}
            className="btn btn-secondary"
            style={{ fontSize: '0.8125rem', padding: '6px 12px' }}
          >
            "Swiggy dinner" (₹350)
          </button>
          <button
            type="button"
            onClick={() => handleQuickPreset('Uber ride to college', 220, 'Uber', 'UPI')}
            className="btn btn-secondary"
            style={{ fontSize: '0.8125rem', padding: '6px 12px' }}
          >
            "Uber ride to college" (₹220)
          </button>
          <button
            type="button"
            onClick={() => handleQuickPreset('Amazon headphones', 1500, 'Amazon', 'Credit Card')}
            className="btn btn-secondary"
            style={{ fontSize: '0.8125rem', padding: '6px 12px' }}
          >
            "Amazon headphones" (₹1,500)
          </button>
        </div>
      </div>

      {/* Main Expense Form */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Expense Details</h2>
            <div className="card-subtitle">
              Enter transaction details and execute Machine Learning classification.
            </div>
          </div>
        </div>

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
            fontSize: '0.875rem',
            marginBottom: '20px'
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
            fontSize: '0.875rem',
            marginBottom: '20px'
          }}>
            <CheckCircle2 size={18} />
            <span>{success}</span>
          </div>
        )}

        <form onSubmit={handlePredict}>
          <div className="form-group">
            <label className="form-label" htmlFor="expense-desc">
              Description <span style={{ color: '#dc2626' }}>*</span>
            </label>
            <input
              id="expense-desc"
              type="text"
              className="form-input"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="e.g. Swiggy dinner, Uber cab, Grocery refill"
              required
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label" htmlFor="expense-amount">
                Amount (₹) <span style={{ color: '#dc2626' }}>*</span>
              </label>
              <input
                id="expense-amount"
                type="number"
                step="any"
                min="1"
                className="form-input"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="350"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="expense-date">
                Transaction Date
              </label>
              <input
                id="expense-date"
                type="date"
                className="form-input"
                value={expenseDate}
                onChange={(e) => setExpenseDate(e.target.value)}
                required
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label" htmlFor="expense-pm">
                Payment Method
              </label>
              <select
                id="expense-pm"
                className="form-select"
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
              >
                {PAYMENT_METHODS.map((pm) => (
                  <option key={pm} value={pm}>{pm}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="expense-merch">
                Merchant / Store (Optional)
              </label>
              <input
                id="expense-merch"
                type="text"
                className="form-input"
                value={merchant}
                onChange={(e) => setMerchant(e.target.value)}
                placeholder="e.g. Swiggy, Amazon, Bescom"
              />
            </div>
          </div>

          <div style={{ marginTop: '12px', display: 'flex', gap: '12px' }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={predicting || !description.trim() || !amount}
              style={{ flex: 1, padding: '12px' }}
            >
              <Sparkles size={16} />
              <span>{predicting ? 'Analyzing...' : 'Predict Category'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* AI Prediction Result Box */}
      {predictionResult && (
        <div className="card" style={{
          borderColor: '#93c5fd',
          backgroundColor: '#f8fafc',
          borderWidth: '2px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '6px',
                backgroundColor: '#2563eb',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Sparkles size={16} />
              </div>
              <span style={{ fontSize: '0.875rem', fontWeight: 700, color: '#1e3a8a', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
                AI Prediction
              </span>
            </div>

            <span className="badge badge-blue">
              {predictionResult.model_name}
            </span>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px',
            backgroundColor: '#ffffff',
            padding: '20px',
            borderRadius: '10px',
            border: '1px solid #e2e8f0',
            marginBottom: '20px'
          }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
                Predicted Category
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#2563eb', marginTop: '4px', textTransform: 'uppercase' }}>
                {predictionResult.category}
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
                Transaction Amount
              </div>
              <div className="financial-value" style={{ fontSize: '1.5rem', color: '#0f172a', marginTop: '4px' }}>
                {formatCurrency(amount)}
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
                Model Confidence
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#16a34a', marginTop: '4px' }}>
                {(predictionResult.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* User Confirmation & Category Override Selector */}
          <div style={{ marginBottom: '20px' }}>
            <label className="form-label" style={{ fontWeight: 600, color: '#0f172a' }}>
              Confirm or Modify Category Before Saving:
            </label>
            <select
              className="form-select"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              style={{ backgroundColor: '#ffffff', fontWeight: 500 }}
            >
              {categories.map((c) => (
                <option key={c.category_id} value={c.name}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={handleConfirmAndSave}
              className="btn btn-primary"
              disabled={saving}
              style={{ flex: 1, padding: '12px' }}
            >
              <CheckCircle2 size={16} />
              <span>{saving ? 'Saving to Oracle Database...' : 'Confirm & Save'}</span>
            </button>

            <button
              type="button"
              onClick={() => setPredictionResult(null)}
              className="btn btn-secondary"
              disabled={saving}
            >
              <RotateCcw size={16} />
              <span>Reset</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
