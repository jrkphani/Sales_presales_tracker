import React from 'react';
import './DashboardTabs.css';

const DashboardTabs = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'region', label: 'Revenue by Region' },
    { id: 'funnel', label: 'Sales Funnel' },
    { id: 'agents', label: 'Agent Performance' },
  ];
  
  return (
    <div className="tabs-container">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => setActiveTab(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
};

export default DashboardTabs;
