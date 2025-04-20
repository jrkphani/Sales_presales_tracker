import React, { useState } from 'react';
import FunnelChart from '../charts/FunnelChart';
import './DashboardPanels.css';

const SalesFunnel = ({ data, formatCurrency }) => {
  // Get available regions from the data
  const regions = Object.keys(data);
  const [selectedRegion, setSelectedRegion] = useState(regions[0] || '');

  // Transform stage data for the funnel chart
  const transformStageData = (stages) => {
    return stages.map(stage => ({
      name: stage.name,
      value: stage.value,
      count: stage.count
    })).sort((a, b) => b.value - a.value);
  };

  const handleRegionChange = (event) => {
    setSelectedRegion(event.target.value);
  };

  const stageData = transformStageData(data[selectedRegion]?.stages || []);
  
  return (
    <div className="funnel-panel">
      <div className="panel-header">
        <h2 className="panel-title">Sales Pipeline by Stage</h2>
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
        <div className="card-content">
          <FunnelChart data={stageData} formatCurrency={formatCurrency} />
        </div>
        
        <div className="stage-breakdown">
          <h3>Stage Details</h3>
          <div className="stage-metrics">
            {stageData.map(stage => (
              <div key={stage.name} className="stage-metric">
                <div className="stage-header">
                  <span className="stage-name">{stage.name}</span>
                  <span className="stage-count">{stage.count} deals</span>
                </div>
                <div className="stage-value">{formatCurrency(stage.value)}</div>
                <div className="stage-progress-bar">
                  <div 
                    className="stage-progress" 
                    style={{ 
                      width: `${(stage.value / stageData[0].value) * 100}%`,
                      backgroundColor: stage.name.toLowerCase().includes('closed') ? '#38a169' : '#1a56db'
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SalesFunnel;
