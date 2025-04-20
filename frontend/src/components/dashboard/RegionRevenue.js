import React, { useState } from 'react';
import BarChart from '../charts/BarChart';
import './DashboardPanels.css';

const RegionRevenue = ({ data, formatCurrency }) => {
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [selectedDeals, setSelectedDeals] = useState([]);
  
  // Get unique regions from the data
  const regions = Object.values(data).reduce((acc, quarterData) => {
    Object.keys(quarterData).forEach(region => {
      if (!acc.includes(region)) {
        acc.push(region);
      }
    });
    return acc;
  }, []);

  // Transform pipeline data for chart
  const transformDataForChart = () => {
    return Object.entries(data).map(([quarter, regions]) => {
      const quarterData = {
        quarter,
        ...Object.entries(regions).reduce((acc, [region, data]) => {
          acc[`${region}_value`] = data.value;
          acc[`${region}_count`] = data.count;
          return acc;
        }, {})
      };
      return quarterData;
    });
  };

  const handleChartClick = (data) => {
    if (data && data.activePayload && data.activePayload.length) {
      const quarter = data.activePayload[0].payload.quarter;
      const regionData = Object.entries(data[quarter] || {})
        .filter(([key]) => !key.includes('_count'))
        .map(([region, value]) => ({
          region: region.replace('_value', ''),
          value
        }));
      setSelectedRegion(quarter);
      setSelectedDeals(regionData);
    }
  };
  
  const resetSelection = () => {
    setSelectedRegion(null);
    setSelectedDeals([]);
  };
  
  const chartData = transformDataForChart();
  
  // Generate keys for the chart based on actual regions
  const chartKeys = regions.map(region => `${region}_value`);
  // Generate colors for each region (you might want to customize this)
  const chartColors = regions.map((_, index) => {
    const hue = (index * 137.5) % 360; // Golden angle approximation for good color distribution
    return `hsl(${hue}, 70%, 50%)`;
  });
  
  return (
    <div className="region-panel">
      <div className="panel-header">
        <h2 className="panel-title">Revenue by Region</h2>
        {selectedRegion && (
          <button className="btn btn-secondary" onClick={resetSelection}>
            ← Back to all regions
          </button>
        )}
      </div>
      
      {!selectedRegion ? (
        <div className="card">
          <div className="card-content">
            <p className="chart-instruction">Click on a quarter to see detailed breakdown</p>
            <BarChart 
              data={chartData}
              keys={chartKeys}
              colors={chartColors}
              onClick={handleChartClick}
              formatCurrency={formatCurrency}
            />
          </div>
        </div>
      ) : (
        <div>
          <div className="region-summary card">
            <h3 className="region-title">{selectedRegion}</h3>
            <div className="region-metrics">
              {selectedDeals.map(deal => (
                <div key={deal.region} className="region-metric">
                  <span className="metric-label">{deal.region}:</span>
                  <span className="metric-value">
                    {formatCurrency(deal.value)}
                  </span>
                  <span className="metric-count">
                    ({data[selectedRegion][deal.region].count} deals)
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RegionRevenue;
