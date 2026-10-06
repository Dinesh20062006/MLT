import React from 'react';
import { Menu, Database, Cpu } from 'lucide-react';

export const Navbar = ({ title, subtitle, onToggleSidebar }) => {
  return (
    <header style={{
      height: '68px',
      backgroundColor: '#ffffff',
      borderBottom: '1px solid #e2e8f0',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 28px',
      position: 'sticky',
      top: 0,
      zIndex: 30
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button
          onClick={onToggleSidebar}
          style={{
            display: 'none',
            background: 'none',
            border: '1px solid #e2e8f0',
            borderRadius: '6px',
            padding: '6px',
            cursor: 'pointer',
            color: '#475569'
          }}
          className="mobile-menu-btn"
          aria-label="Toggle navigation menu"
        >
          <Menu size={20} />
        </button>

        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#0f172a', margin: 0 }}>
            {title}
          </h1>
          {subtitle && (
            <div style={{ fontSize: '0.8125rem', color: '#64748b' }}>
              {subtitle}
            </div>
          )}
        </div>
      </div>

      {/* System Status Badges */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          backgroundColor: '#f8fafc',
          border: '1px solid #e2e8f0',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          color: '#475569'
        }}>
          <Database size={13} color="#2563eb" />
          <span>Oracle 21c XE</span>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          backgroundColor: '#f0fdf4',
          border: '1px solid #bbf7d0',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          color: '#16a34a',
          fontWeight: 500
        }}>
          <Cpu size={13} color="#16a34a" />
          <span>Hybrid ML Model</span>
        </div>
      </div>
    </header>
  );
};
