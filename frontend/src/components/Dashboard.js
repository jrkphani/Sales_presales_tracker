import React, { useEffect, useState } from 'react';
import '../styles/Dashboard.css';
import { getDashboardData } from '../services/data/sales-data-service';
import RegionRevenue from './dashboard/RegionRevenue';
import SalesFunnel from './dashboard/SalesFunnel';
import OverviewPanel from './dashboard/OverviewPanel';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState({
        // Initial state structure (will be replaced with real data)
        regional_pipeline: {
            Q1: { APAC: { value: 0, count: 0 }, EMEA: { value: 0, count: 0 }, Americas: { value: 0, count: 0 } },
            Q2: { APAC: { value: 0, count: 0 }, EMEA: { value: 0, count: 0 }, Americas: { value: 0, count: 0 } },
            Q3: { APAC: { value: 0, count: 0 }, EMEA: { value: 0, count: 0 }, Americas: { value: 0, count: 0 } },
            Q4: { APAC: { value: 0, count: 0 }, EMEA: { value: 0, count: 0 }, Americas: { value: 0, count: 0 } }
        },
        stage_region_breakdown: {
            APAC: { stages: [] },
            EMEA: { stages: [] },
            Americas: { stages: [] }
        },
        en_nn_split: {
            APAC: { EN: { value: 0, count: 0 }, NN: { value: 0, count: 0 } },
            EMEA: { EN: { value: 0, count: 0 }, NN: { value: 0, count: 0 } },
            Americas: { EN: { value: 0, count: 0 }, NN: { value: 0, count: 0 } }
        },
        revenue_projection: {
            APAC: { quota: 0, achieved: 0, projected_80: 0, projected_all: 0 },
            EMEA: { quota: 0, achieved: 0, projected_80: 0, projected_all: 0 },
            Americas: { quota: 0, achieved: 0, projected_80: 0, projected_all: 0 }
        },
        potential_closures: {
            APAC: [],
            EMEA: [],
            Americas: []
        },
        opportunity_types: {
            APAC: { POC: { value: 0, count: 0 }, MAP: { value: 0, count: 0 }, GenAI: { value: 0, count: 0 } },
            EMEA: { POC: { value: 0, count: 0 }, MAP: { value: 0, count: 0 }, GenAI: { value: 0, count: 0 } },
            Americas: { POC: { value: 0, count: 0 }, MAP: { value: 0, count: 0 }, GenAI: { value: 0, count: 0 } }
        },
        stage_movement: {
            APAC: [],
            EMEA: [],
            Americas: []
        },
        financial_year: ''
    });
    
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-SG', {
            style: 'currency',
            currency: 'SGD',
            maximumFractionDigits: 0
        }).format(value);
    };

    const formatDateRange = (startDate, endDate) => {
        const start = new Date(startDate);
        const end = new Date(endDate);
        return `${start.toLocaleDateString('en-SG')} - ${end.toLocaleDateString('en-SG')}`;
    };

    // Get financial year quarter dates
    const getFinancialYearQuarterDates = () => {
        const now = new Date();
        const currentMonth = now.getMonth(); // 0-11
        const currentYear = now.getFullYear();
        
        // Determine financial year
        const financialYearStart = currentMonth < 3 ? currentYear - 1 : currentYear;
        const financialYearEnd = financialYearStart + 1;
        
        // Q1: Apr-Jun, Q2: Jul-Sep, Q3: Oct-Dec, Q4: Jan-Mar
        return {
            Q1: {
                start: new Date(financialYearStart, 3, 1), // April 1
                end: new Date(financialYearStart, 5, 30)   // June 30
            },
            Q2: {
                start: new Date(financialYearStart, 6, 1), // July 1
                end: new Date(financialYearStart, 8, 30)   // September 30
            },
            Q3: {
                start: new Date(financialYearStart, 9, 1), // October 1
                end: new Date(financialYearStart, 11, 31)  // December 31
            },
            Q4: {
                start: new Date(financialYearEnd, 0, 1),   // January 1
                end: new Date(financialYearEnd, 2, 31)     // March 31
            }
        };
    };

    // Fetch data from Zoho CRM API
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const data = await getDashboardData();
                setDashboardData(data);
                setError(null);
            } catch (err) {
                console.error('Error fetching dashboard data:', err);
                setError('Failed to load dashboard data. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="dashboard loading">
                <div className="loading-spinner">Loading dashboard data...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="dashboard error">
                <div className="error-message">{error}</div>
            </div>
        );
    }

    const quarterDates = getFinancialYearQuarterDates();

    return (
        <div className="dashboard">
            <header className="header">
                <h1>Sales Dashboard</h1>
                <div className="financial-year">
                    <h2>Financial Year: {dashboardData.financial_year}</h2>
                </div>
                <div className="date-ranges">
                    <span>Q1: {formatDateRange(quarterDates.Q1.start, quarterDates.Q1.end)}</span>
                    <span>Q2: {formatDateRange(quarterDates.Q2.start, quarterDates.Q2.end)}</span>
                    <span>Q3: {formatDateRange(quarterDates.Q3.start, quarterDates.Q3.end)}</span>
                    <span>Q4: {formatDateRange(quarterDates.Q4.start, quarterDates.Q4.end)}</span>
                </div>
            </header>

            <div className="dashboard-grid">
                <OverviewPanel data={dashboardData} formatCurrency={formatCurrency} />
                <RegionRevenue data={dashboardData.regional_pipeline} formatCurrency={formatCurrency} />
                <SalesFunnel data={dashboardData.stage_region_breakdown} formatCurrency={formatCurrency} />
            </div>
        </div>
    );
};

export default Dashboard; 