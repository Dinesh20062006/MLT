import React, { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';

const PAGE_META = {
  '/dashboard': {
    title: 'Financial Overview',
    subtitle: 'Track your income, expenses and savings.'
  },
  '/add-expense': {
    title: 'Add New Expense',
    subtitle: 'AI-assisted expense categorization and transaction logging.'
  },
  '/history': {
    title: 'Expense History',
    subtitle: 'Browse, search, and manage all your stored transactions.'
  },
  '/analytics': {
    title: 'Financial Analytics',
    subtitle: 'Deep dive into spending distributions, savings rates, and timelines.'
  },
  '/model-comparison': {
    title: 'Model Comparison',
    subtitle: 'Evaluate experimental benchmark metrics and the proposed hybrid classifier.'
  },
  '/settings': {
    title: 'Settings',
    subtitle: 'Configure your monthly income and preferences.'
  }
};

export const AppLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const currentMeta = PAGE_META[location.pathname] || {
    title: 'Smart Expense',
    subtitle: 'Intelligent expense classification and financial insights.'
  };

  return (
    <div className="app-container">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      <div className="main-content">
        <Navbar
          title={currentMeta.title}
          subtitle={currentMeta.subtitle}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />
        
        <main className="content-body">
          <Outlet />
        </main>
      </div>

      <style>{`
        @media (max-width: 768px) {
          .sidebar-desktop {
            display: none !important;
          }
          .mobile-menu-btn {
            display: flex !important;
          }
        }
        @media (min-width: 769px) {
          .sidebar-desktop {
            display: flex !important;
          }
          .mobile-menu-btn {
            display: none !important;
          }
        }
      `}</style>
    </div>
  );
};
