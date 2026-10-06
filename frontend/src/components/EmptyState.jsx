import React from 'react';
import { Inbox, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';

export const EmptyState = ({
  title = 'No expenses yet',
  description = 'Add your first transaction to unlock smart category predictions and financial analytics.',
  actionText = 'Add Your First Expense',
  actionLink = '/add-expense',
  icon: Icon = Inbox
}) => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      padding: '48px 24px',
      backgroundColor: '#ffffff',
      border: '1px dashed #cbd5e1',
      borderRadius: '12px'
    }}>
      <div style={{
        width: '48px',
        height: '48px',
        borderRadius: '50%',
        backgroundColor: '#f1f5f9',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#64748b',
        marginBottom: '16px'
      }}>
        <Icon size={24} />
      </div>

      <h3 style={{ fontSize: '1.05rem', fontWeight: 600, color: '#0f172a', marginBottom: '6px' }}>
        {title}
      </h3>

      <p style={{ maxWidth: '400px', fontSize: '0.875rem', color: '#64748b', marginBottom: '20px' }}>
        {description}
      </p>

      {actionLink && actionText && (
        <Link to={actionLink} className="btn btn-primary">
          <Plus size={16} />
          <span>{actionText}</span>
        </Link>
      )}
    </div>
  );
};
