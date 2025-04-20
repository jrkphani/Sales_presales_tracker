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

// Default currency formatter if none is provided
const defaultFormatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

const CustomTooltip = ({ active, payload, formatCurrency = defaultFormatCurrency }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="custom-tooltip">
        <p className="label">{data.name}</p>
        <p className="value">Value: {formatCurrency(data.value)}</p>
        <p className="deals">Deals: {data.deals}</p>
      </div>
    );
  }
  return null;
};

const AgentChart = ({ data, formatCurrency }) => {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip content={<CustomTooltip formatCurrency={formatCurrency} />} />
        <Legend />
        <Bar 
          dataKey="value" 
          name="Deal Value" 
          fill="#1a56db" 
          radius={[4, 4, 0, 0]} 
        />
        <Bar 
          dataKey="deals" 
          name="Deal Count" 
          fill="#7e3af2" 
          radius={[4, 4, 0, 0]} 
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default AgentChart;
