import React from 'react';
import BarChart from '../charts/BarChart';
import FunnelChart from '../charts/FunnelChart';
import AgentChart from '../charts/AgentChart';
import './DashboardPanels.css';

const OverviewPanel = ({ data, formatCurrency }) => {
  // Calculate metrics from real data
  const calculateMetrics = () => {
    // Sum up all regional pipeline values for the current quarter
    const currentQuarter = getCurrentQuarter();
    const totalPipelineValue = Object.values(data.regional_pipeline[currentQuarter])
      .reduce((sum, region) => sum + region.value, 0);
    
    // Count total opportunities
    const totalOpportunities = Object.values(data.regional_pipeline[currentQuarter])
      .reduce((sum, region) => sum + region.count, 0);
    
    // Calculate average deal size
    const avgDealSize = totalPipelineValue / (totalOpportunities || 1);
    
    // Calculate win rate from stage breakdown
    const totalWonValue = Object.values(data.stage_region_breakdown)
      .reduce((sum, region) => {
        const wonStage = region.stages.find(stage => stage.name === 'Closed Won');
        return sum + (wonStage?.value || 0);
      }, 0);
    const winRate = (totalWonValue / totalPipelineValue * 100).toFixed(1);

    return {
      totalPipelineValue,
      totalOpportunities,
      avgDealSize,
      winRate
    };
  };

  const getCurrentQuarter = () => {
    const now = new Date();
    const month = now.getMonth();
    if (month >= 3 && month <= 5) return 'Q1';
    if (month >= 6 && month <= 8) return 'Q2';
    if (month >= 9 && month <= 11) return 'Q3';
    return 'Q4';
  };

  const metrics = calculateMetrics();
  
  // Transform region data for the chart - dynamically map from real data
  const currentQuarter = getCurrentQuarter();
  const regionData = Object.entries(data.regional_pipeline[currentQuarter]).map(([region, regionData]) => ({
    region,
    revenue: regionData.value,
    targetRevenue: regionData.value * 1.2 // Using 20% above current as target, adjust as needed
  }));

  // Transform funnel data for the chart
  const funnelData = Object.values(data.stage_region_breakdown)
    .flatMap(region => region.stages)
    .reduce((acc, stage) => {
      const existingStage = acc.find(s => s.stage === stage.name);
      if (existingStage) {
        existingStage.value += stage.value;
        existingStage.count += stage.count;
      } else {
        acc.push({
          stage: stage.name,
          value: stage.value,
          count: stage.count
        });
      }
      return acc;
    }, [])
    .sort((a, b) => b.value - a.value); // Sort by value in descending order

  // Transform agent data for the chart
  const agentData = Object.values(data.potential_closures)
    .flatMap(deals => deals)
    .reduce((acc, deal) => {
      const existing = acc.find(item => item.name === deal.name);
      if (existing) {
        existing.value += deal.value;
        existing.deals++;
      } else {
        acc.push({
          name: deal.name,
          value: deal.value,
          deals: 1
        });
      }
      return acc;
    }, [])
    .sort((a, b) => b.value - a.value); // Sort by value in descending order
  
  return (
    <div className="overview-panel">
      <h2 className="panel-title">Sales Dashboard Overview</h2>
      
      {/* Key Metrics Row */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-title">Total Pipeline Value</div>
          <div className="metric-value">{formatCurrency(metrics.totalPipelineValue)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-title">Total Opportunities</div>
          <div className="metric-value">{metrics.totalOpportunities}</div>
        </div>
        <div className="metric-card">
          <div className="metric-title">Average Deal Size</div>
          <div className="metric-value">{formatCurrency(metrics.avgDealSize)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-title">Win Rate</div>
          <div className="metric-value">{metrics.winRate}%</div>
        </div>
      </div>
      
      {/* Charts Section */}
      <div className="charts-grid">
        <div className="card">
          <h3 className="card-title">Revenue by Region</h3>
          <BarChart 
            data={regionData} 
            keys={['revenue', 'targetRevenue']} 
            colors={['#1a56db', '#cbd5e0']} 
            formatCurrency={formatCurrency}
            xAxisKey="region"
          />
        </div>
        <div className="card">
          <h3 className="card-title">Sales Funnel</h3>
          <FunnelChart data={funnelData} formatCurrency={formatCurrency} />
        </div>
      </div>
    </div>
  );
};

export default OverviewPanel;
