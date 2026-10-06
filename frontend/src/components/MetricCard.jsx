import React from 'react';

export const MetricCard = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  colorScheme = 'blue',
  badge
}) => {
  const schemeStyles = {
    blue: {
      iconBg: '#eff6ff',
      iconColor: '#2563eb',
      border: '#e2e8f0',
      valueColor: '#0f172a'
    },
    green: {
      iconBg: '#f0fdf4',
      iconColor: '#16a34a',
      border: '#e2e8f0',
      valueColor: '#16a34a'
    },
    red: {
      iconBg: '#fef2f2',
      iconColor: '#dc2626',
      border: '#e2e8f0',
      valueColor: '#dc2626'
    },
    amber: {
      iconBg: '#fffbeb',
      iconColor: '#d97706',
      border: '#e2e8f0',
      valueColor: '#0f172a'
    }
  };

  const currentScheme = schemeStyles[colorScheme] || schemeStyles.blue;

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '0.8125rem', fontWeight: 500, color: '#64748b' }}>
            {title}
          </span>
          {Icon && (
            <div style={{
              width: '34px',
              height: '34px',
              borderRadius: '8px',
              backgroundColor: currentScheme.iconBg,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: currentScheme.iconColor
            }}>
              <Icon size={18} />
            </div>
          )}
        </div>

        <div className="financial-value" style={{ fontSize: '1.625rem', color: currentScheme.valueColor, lineHeight: 1.2 }}>
          {value}
        </div>
      </div>

      {(subtitle || badge) && (
        <div style={{ marginTop: '12px', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem', color: '#64748b' }}>
          {badge && (
            <span className={`badge ${badge.type ? `badge-${badge.type}` : 'badge-gray'}`}>
              {badge.text}
            </span>
          )}
          {subtitle && <span>{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
