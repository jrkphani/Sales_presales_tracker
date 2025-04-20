import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

const CustomTooltip = ({ active, payload, formatCurrency }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip">
        <p className="label">{data.name}</p>
        <p className="value">Value: {formatCurrency(data.value)}</p>
        <p className="count">Deals: {data.count}</p>
      </div>
    );
  }
  return null;
};

const FunnelChart = ({ data, formatCurrency }) => {
  // Debug: log the data to check for name fields
  console.log("FunnelChart data:", data);
  // Sort data to ensure it's in the correct funnel order
  const sortedData = [...data].sort((a, b) => b.value - a.value);
  
  return (
    <ResponsiveContainer width={1200} height={350}>
      <BarChart
        data={sortedData}
        margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        {/* X axis: force horizontal labels, small font */}
        <XAxis 
          type="category" 
          dataKey="stage" 
          angle={-45} 
          textAnchor="end" 
          interval={0} 
          height={70} 
          stroke="#1a202c"
          tick={{ fontSize: 10, fill: "#1a202c" }}
        />
        <YAxis type="number" />
        <Tooltip content={<CustomTooltip formatCurrency={formatCurrency} />} />
        <Legend />
        <Bar 
          dataKey="value" 
          name="Deal Value" 
          fill="#1a56db" 
          radius={[4, 4, 0, 0]}
        />
        <Bar 
          dataKey="count" 
          name="Deal Count" 
          fill="#7e3af2" 
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default FunnelChart;
