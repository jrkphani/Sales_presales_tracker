// Sample data for the sales dashboard

// Sales by region
export const regionData = [
  { region: 'North America', revenue: 1250000, targetRevenue: 1500000 },
  { region: 'Europe', revenue: 890000, targetRevenue: 1000000 },
  { region: 'Asia Pacific', revenue: 750000, targetRevenue: 700000 },
  { region: 'Latin America', revenue: 420000, targetRevenue: 500000 },
  { region: 'Middle East', revenue: 320000, targetRevenue: 350000 },
];

// Sales funnel data
export const funnelData = [
  { stage: 'Lead', count: 750, value: 7500000 },
  { stage: 'Qualified', count: 480, value: 4800000 },
  { stage: 'Proposal', count: 320, value: 3200000 },
  { stage: 'Negotiation', count: 180, value: 1800000 },
  { stage: 'Closed Won', count: 95, value: 950000 },
];

// Sales agent performance
export const agentData = [
  { 
    name: 'Alex Johnson', 
    closedValue: 320000, 
    pipelineValue: 1200000, 
    targetValue: 400000,
    deals: [
      { id: 'AJ001', company: 'TechCorp', value: 85000, stage: 'Closed Won', probability: 100 },
      { id: 'AJ002', company: 'DataSystems', value: 120000, stage: 'Closed Won', probability: 100 },
      { id: 'AJ003', company: 'InnovateTech', value: 65000, stage: 'Closed Won', probability: 100 },
      { id: 'AJ004', company: 'GlobalSolutions', value: 50000, stage: 'Closed Won', probability: 100 },
      { id: 'AJ005', company: 'FutureSoft', value: 220000, stage: 'Negotiation', probability: 80 },
      { id: 'AJ006', company: 'WebGiants', value: 180000, stage: 'Proposal', probability: 60 },
      { id: 'AJ007', company: 'CloudNine', value: 300000, stage: 'Qualified', probability: 40 },
      { id: 'AJ008', company: 'SkyConnect', value: 500000, stage: 'Lead', probability: 20 },
    ]
  },
  { 
    name: 'Maria Garcia', 
    closedValue: 415000, 
    pipelineValue: 950000, 
    targetValue: 400000,
    deals: [
      { id: 'MG001', company: 'RetailPros', value: 95000, stage: 'Closed Won', probability: 100 },
      { id: 'MG002', company: 'ShopWare', value: 140000, stage: 'Closed Won', probability: 100 },
      { id: 'MG003', company: 'MerchantsGroup', value: 180000, stage: 'Closed Won', probability: 100 },
      { id: 'MG004', company: 'StoreConnect', value: 250000, stage: 'Negotiation', probability: 80 },
      { id: 'MG005', company: 'RetailTech', value: 200000, stage: 'Proposal', probability: 60 },
      { id: 'MG006', company: 'ShopifyPlus', value: 300000, stage: 'Qualified', probability: 40 },
      { id: 'MG007', company: 'CartSystems', value: 200000, stage: 'Lead', probability: 20 },
    ]
  },
  { 
    name: 'James Wilson', 
    closedValue: 290000, 
    pipelineValue: 1400000, 
    targetValue: 400000,
    deals: [
      { id: 'JW001', company: 'FinanceGroup', value: 110000, stage: 'Closed Won', probability: 100 },
      { id: 'JW002', company: 'BankTech', value: 95000, stage: 'Closed Won', probability: 100 },
      { id: 'JW003', company: 'InsureTech', value: 85000, stage: 'Closed Won', probability: 100 },
      { id: 'JW004', company: 'WealthManage', value: 300000, stage: 'Negotiation', probability: 80 },
      { id: 'JW005', company: 'CapitalSystems', value: 350000, stage: 'Proposal', probability: 60 },
      { id: 'JW006', company: 'MoneyMatters', value: 250000, stage: 'Qualified', probability: 40 },
      { id: 'JW007', company: 'InvestGroup', value: 500000, stage: 'Lead', probability: 20 },
    ]
  },
  { 
    name: 'Sarah Chen', 
    closedValue: 510000, 
    pipelineValue: 800000, 
    targetValue: 400000,
    deals: [
      { id: 'SC001', company: 'TechInnovate', value: 180000, stage: 'Closed Won', probability: 100 },
      { id: 'SC002', company: 'CloudSystems', value: 150000, stage: 'Closed Won', probability: 100 },
      { id: 'SC003', company: 'DataCorp', value: 180000, stage: 'Closed Won', probability: 100 },
      { id: 'SC004', company: 'NetworkSolutions', value: 220000, stage: 'Negotiation', probability: 80 },
      { id: 'SC005', company: 'ServerTech', value: 300000, stage: 'Proposal', probability: 60 },
      { id: 'SC006', company: 'CloudConnect', value: 280000, stage: 'Lead', probability: 20 },
    ]
  },
  { 
    name: 'Robert Kim', 
    closedValue: 350000, 
    pipelineValue: 1100000, 
    targetValue: 400000,
    deals: [
      { id: 'RK001', company: 'HealthTech', value: 120000, stage: 'Closed Won', probability: 100 },
      { id: 'RK002', company: 'MedicalSystems', value: 130000, stage: 'Closed Won', probability: 100 },
      { id: 'RK003', company: 'PharmaConnect', value: 100000, stage: 'Closed Won', probability: 100 },
      { id: 'RK004', company: 'LifeSciences', value: 250000, stage: 'Negotiation', probability: 80 },
      { id: 'RK005', company: 'BioTech', value: 300000, stage: 'Proposal', probability: 60 },
      { id: 'RK006', company: 'HealthSoft', value: 200000, stage: 'Qualified', probability: 40 },
      { id: 'RK007', company: 'MedicalAI', value: 350000, stage: 'Lead', probability: 20 },
    ]
  },
];

// Deal data by region
export const dealsByRegion = {
  'North America': [
    { id: 'NA001', company: 'TechCorp', value: 85000, stage: 'Closed Won', agent: 'Alex Johnson' },
    { id: 'NA002', company: 'DataSystems', value: 120000, stage: 'Closed Won', agent: 'Alex Johnson' },
    { id: 'NA003', company: 'CloudSystems', value: 150000, stage: 'Closed Won', agent: 'Sarah Chen' },
    { id: 'NA004', company: 'NetworkSolutions', value: 220000, stage: 'Negotiation', agent: 'Sarah Chen' },
    { id: 'NA005', company: 'GlobalSolutions', value: 50000, stage: 'Closed Won', agent: 'Alex Johnson' },
    { id: 'NA006', company: 'HealthTech', value: 120000, stage: 'Closed Won', agent: 'Robert Kim' },
    { id: 'NA007', company: 'SkyConnect', value: 500000, stage: 'Lead', agent: 'Alex Johnson' },
  ],
  'Europe': [
    { id: 'EU001', company: 'RetailPros', value: 95000, stage: 'Closed Won', agent: 'Maria Garcia' },
    { id: 'EU002', company: 'FinanceGroup', value: 110000, stage: 'Closed Won', agent: 'James Wilson' },
    { id: 'EU003', company: 'BankTech', value: 95000, stage: 'Closed Won', agent: 'James Wilson' },
    { id: 'EU004', company: 'ShopWare', value: 140000, stage: 'Closed Won', agent: 'Maria Garcia' },
    { id: 'EU005', company: 'CapitalSystems', value: 350000, stage: 'Proposal', agent: 'James Wilson' },
    { id: 'EU006', company: 'RetailTech', value: 200000, stage: 'Proposal', agent: 'Maria Garcia' },
  ],
  'Asia Pacific': [
    { id: 'AP001', company: 'TechInnovate', value: 180000, stage: 'Closed Won', agent: 'Sarah Chen' },
    { id: 'AP002', company: 'DataCorp', value: 180000, stage: 'Closed Won', agent: 'Sarah Chen' },
    { id: 'AP003', company: 'InnovateTech', value: 65000, stage: 'Closed Won', agent: 'Alex Johnson' },
    { id: 'AP004', company: 'ServerTech', value: 300000, stage: 'Proposal', agent: 'Sarah Chen' },
    { id: 'AP005', company: 'CloudConnect', value: 280000, stage: 'Lead', agent: 'Sarah Chen' },
  ],
  'Latin America': [
    { id: 'LA001', company: 'MerchantsGroup', value: 180000, stage: 'Closed Won', agent: 'Maria Garcia' },
    { id: 'LA002', company: 'InsureTech', value: 85000, stage: 'Closed Won', agent: 'James Wilson' },
    { id: 'LA003', company: 'StoreConnect', value: 250000, stage: 'Negotiation', agent: 'Maria Garcia' },
    { id: 'LA004', company: 'ShopifyPlus', value: 300000, stage: 'Qualified', agent: 'Maria Garcia' },
  ],
  'Middle East': [
    { id: 'ME001', company: 'PharmaConnect', value: 100000, stage: 'Closed Won', agent: 'Robert Kim' },
    { id: 'ME002', company: 'MedicalSystems', value: 130000, stage: 'Closed Won', agent: 'Robert Kim' },
    { id: 'ME003', company: 'LifeSciences', value: 250000, stage: 'Negotiation', agent: 'Robert Kim' },
    { id: 'ME004', company: 'BioTech', value: 300000, stage: 'Proposal', agent: 'Robert Kim' },
  ]
};

// Helper to calculate key metrics
export const calculateMetrics = () => {
  const totalPipelineValue = agentData.reduce((total, agent) => total + agent.pipelineValue, 0);
  const closedWonValue = agentData.reduce((total, agent) => total + agent.closedValue, 0);
  const totalOpportunities = agentData.reduce(
    (total, agent) => total + agent.deals.length, 
    0
  );
  const avgDealSize = closedWonValue / funnelData.find(item => item.stage === 'Closed Won').count;
  
  return {
    totalPipelineValue,
    closedWonValue,
    totalOpportunities,
    avgDealSize,
    winRate: (funnelData.find(item => item.stage === 'Closed Won').count / funnelData.find(item => item.stage === 'Lead').count * 100).toFixed(1)
  };
};

// Format currency
export const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};
