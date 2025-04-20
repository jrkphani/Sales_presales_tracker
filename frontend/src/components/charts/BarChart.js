import React from 'react';
import {
  ResponsiveContainer,
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

// CustomTooltip component that receives formatCurrency directly as a prop
const CustomTooltip = ({ active, payload, label, formatCurrency }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        {payload.map((entry, index) => (
          <p key={index} className="tooltip-value" style={{ color: entry.color }}>
            {entry.name}: {formatCurrency(entry.value)}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const BarChart = ({ data, keys, colors, onClick, formatCurrency, xAxisKey = 'quarter' }) => {
  // Debug: log the data and keys to check for x-axis issues
  console.log("BarChart data:", data);
  console.log("BarChart keys:", keys);
  // No need to add formatCurrency to each data point since we pass it directly to CustomTooltip
  const enhancedData = data;

  return (
    <ResponsiveContainer width="100%" height={350}>
      <RechartsBarChart
        data={enhancedData}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        onClick={onClick}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xAxisKey} />
        <YAxis />
        <Tooltip content={props => <CustomTooltip {...props} formatCurrency={formatCurrency} />} />
        <Legend />
        {keys.map((key, index) => (
          <Bar
            key={key}
            dataKey={key}
            name={key.split('_')[0]}
            fill={colors[index]}
            radius={[4, 4, 0, 0]}
          />
        ))}
      </RechartsBarChart>
    </ResponsiveContainer>
  );
};

export default BarChart;
