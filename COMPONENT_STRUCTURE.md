# Component Structure

## Layout Components
- `DashboardTabs.js` - Navigation tabs for switching between dashboard views
- `MetricsCard.js` - Reusable component for displaying key metrics with labels and values

## Chart Components
- `BarChart.js` - Reusable bar chart component with customizable tooltips and click handling
- `FunnelChart.js` - Horizontal bar chart configured for funnel visualization
- `AgentChart.js` - Stacked bar chart for agent performance with target reference line

## Dashboard Components
- `OverviewPanel.js` - Main dashboard with summary metrics and charts
- `RegionRevenue.js` - Regional performance analysis with drill-down capability
- `SalesFunnel.js` - Sales pipeline visualization with conversion rates
- `AgentPerformance.js` - Individual agent performance tracking

## Data and Utilities
- `sampleData.js` - Contains sample data structures and helper functions for formatting
- `formatters.js` - Utility functions for data formatting (currency, percentages, etc.)
- `calculations.js` - Functions for deriving metrics from raw data

## Component Hierarchy
```
App
├── DashboardTabs
├── OverviewPanel
│   ├── MetricsCard (multiple)
│   ├── BarChart (Revenue by Region)
│   ├── FunnelChart (Sales Funnel)
│   └── AgentChart (Agent Performance)
│
├── RegionRevenue
│   ├── BarChart
│   └── DataTable (deal details)
│
├── SalesFunnel
│   ├── FunnelChart
│   ├── ConversionRates
│   └── DataTable (deal details)
│
└── AgentPerformance
    ├── AgentChart
    ├── MetricsCard (multiple)
    └── DataTable (deal details)
```

## Component Data Flow
- App.js maintains the active tab state
- Each dashboard panel manages its own drill-down state
- Chart components accept data and callback functions as props
- Helper functions in sampleData.js provide formatted data and calculations

## Component Prop Structure

### Chart Components

#### BarChart
```javascript
{
  data: Array,           // Data array for the chart
  keys: Array,           // Data keys to display as bars
  colors: Array,         // Colors for each bar
  onClick: Function      // Click handler for drill-down
}
```

#### FunnelChart
```javascript
{
  data: Array,           // Funnel stage data
  onClick: Function      // Click handler for stage selection
}
```

#### AgentChart
```javascript
{
  data: Array,           // Agent performance data
  onClick: Function      // Click handler for agent selection
}
```

### Dashboard Components

#### Common Props Pattern
```javascript
{
  data: Array,           // Data specific to the component
  onDrillDown: Function, // Handler for drill-down actions
  onReset: Function,     // Handler to reset selection
  selectedItem: Object   // Currently selected item for drill-down view
}
```
