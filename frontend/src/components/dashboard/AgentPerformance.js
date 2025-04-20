import React, { useState } from 'react';
import AgentChart from '../charts/AgentChart';
import './DashboardPanels.css';

const AgentPerformance = ({ data, formatCurrency }) => {
  // Get available regions from the data
  const regions = Object.keys(data.potential_closures);
  const [selectedRegion, setSelectedRegion] = useState(regions[0] || '');

  // Transform agent data for the chart
  const transformAgentData = () => {
    const deals = data.potential_closures[selectedRegion] || [];
    const agentPerformance = {};

    // Aggregate deals by agent
    deals.forEach(deal => {
      if (!agentPerformance[deal.name]) {
        agentPerformance[deal.name] = {
          name: deal.name,
          value: 0,
          deals: 0
        };
      }
      agentPerformance[deal.name].value += deal.value;
      agentPerformance[deal.name].deals++;
    });

    return Object.values(agentPerformance).sort((a, b) => b.value - a.value);
  };

  const handleRegionChange = (event) => {
    setSelectedRegion(event.target.value);
  };

  const agentData = transformAgentData();
  const totalValue = agentData.reduce((sum, agent) => sum + agent.value, 0);
  const totalDeals = agentData.reduce((sum, agent) => sum + agent.deals, 0);

  return (
    <div className="agent-panel">
      <div className="panel-header">
        <h2 className="panel-title">Agent Performance</h2>
        <select 
          className="region-select" 
          value={selectedRegion} 
          onChange={handleRegionChange}
        >
          {regions.map(region => (
            <option key={region} value={region}>{region}</option>
          ))}
        </select>
      </div>

      <div className="card">
        <div className="region-summary">
          <h3>{selectedRegion} Region Overview</h3>
          <div className="summary-metrics">
            <div className="summary-metric">
              <span className="metric-label">Total Value:</span>
              <span className="metric-value">{formatCurrency(totalValue)}</span>
            </div>
            <div className="summary-metric">
              <span className="metric-label">Total Deals:</span>
              <span className="metric-value">{totalDeals}</span>
            </div>
            <div className="summary-metric">
              <span className="metric-label">Average Deal Size:</span>
              <span className="metric-value">
                {formatCurrency(totalDeals > 0 ? totalValue / totalDeals : 0)}
              </span>
            </div>
          </div>
        </div>
        <AgentChart data={agentData} formatCurrency={formatCurrency} />
      </div>
    </div>
  );
};

export default AgentPerformance;
