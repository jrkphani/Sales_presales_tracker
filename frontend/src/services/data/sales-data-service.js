// Sales data service for processing current-data.json

/**
 * Transform raw deals data into dashboard format
 * @param {Array} deals - Array of deal objects from current-data.json
 * @returns {Object} Transformed dashboard data
 */
function transformDealsToDashboardData(deals) {
    // Get unique regions from the deals
    const uniqueRegions = [...new Set(deals.map(deal => deal.Region || 'Unassigned'))];
    
    const dashboardData = {
        regional_pipeline: initializeRegionalPipeline(uniqueRegions),
        stage_region_breakdown: initializeRegionBreakdown(uniqueRegions),
        en_nn_split: initializeENNNSplit(uniqueRegions),
        revenue_projection: initializeRevenueProjection(uniqueRegions),
        potential_closures: initializePotentialClosures(uniqueRegions),
        opportunity_types: initializeOpportunityTypes(uniqueRegions),
        stage_movement: initializeStageMovement(uniqueRegions),
        financial_year: getCurrentFinancialYear()
    };

    // Process each deal
    deals.forEach(deal => {
        const amount = parseFloat(deal.Amount) || 0;
        const region = deal.Region || 'Unassigned';
        const quarter = getQuarterFromDate(deal.Closing_Date);
        
        // Update regional pipeline
        if (quarter && dashboardData.regional_pipeline[quarter][region]) {
            dashboardData.regional_pipeline[quarter][region].value += amount;
            dashboardData.regional_pipeline[quarter][region].count++;
        }

        // Update stage breakdown
        updateStageBreakdown(dashboardData.stage_region_breakdown[region], deal.Stage, amount);

        // Update EN/NN split
        const dealType = deal.Type || '';
        const isEN = dealType.includes('EN') || dealType.includes('Existing');
        const splitCategory = isEN ? 'EN' : 'NN';
        dashboardData.en_nn_split[region][splitCategory].value += amount;
        dashboardData.en_nn_split[region][splitCategory].count++;

        // Update revenue projection
        updateRevenueProjection(dashboardData.revenue_projection[region], deal);

        // Update potential closures
        if (isPotentialClosure(deal)) {
            dashboardData.potential_closures[region].push({
                name: deal.Deal_Name,
                value: amount,
                stage: deal.Stage,
                action: determineAction(deal)
            });
        }

        // Update opportunity types
        updateOpportunityTypes(dashboardData.opportunity_types[region], deal.Type, amount);
    });

    return dashboardData;
}

// Helper functions
function initializeRegionalPipeline(regions) {
    const quarters = ['Q1', 'Q2', 'Q3', 'Q4'];
    return quarters.reduce((acc, quarter) => {
        acc[quarter] = regions.reduce((regionAcc, region) => {
            regionAcc[region] = { value: 0, count: 0 };
            return regionAcc;
        }, {});
        return acc;
    }, {});
}

function initializeRegionBreakdown(regions) {
    return regions.reduce((acc, region) => {
        acc[region] = { stages: [] };
        return acc;
    }, {});
}

function initializeENNNSplit(regions) {
    return regions.reduce((acc, region) => {
        acc[region] = { 
            EN: { value: 0, count: 0 }, 
            NN: { value: 0, count: 0 } 
        };
        return acc;
    }, {});
}

function initializeRevenueProjection(regions) {
    return regions.reduce((acc, region) => {
        acc[region] = { 
            quota: 0, 
            achieved: 0, 
            projected_80: 0, 
            projected_all: 0 
        };
        return acc;
    }, {});
}

function initializePotentialClosures(regions) {
    return regions.reduce((acc, region) => {
        acc[region] = [];
        return acc;
    }, {});
}

function initializeOpportunityTypes(regions) {
    return regions.reduce((acc, region) => {
        acc[region] = { 
            POC: { value: 0, count: 0 }, 
            MAP: { value: 0, count: 0 }, 
            GenAI: { value: 0, count: 0 } 
        };
        return acc;
    }, {});
}

function initializeStageMovement(regions) {
    return regions.reduce((acc, region) => {
        acc[region] = [];
        return acc;
    }, {});
}

function getCurrentFinancialYear() {
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const startYear = currentMonth < 3 ? currentYear - 1 : currentYear;
    return `${startYear}-${startYear + 1}`;
}

function getQuarterFromDate(dateString) {
    if (!dateString) return null;
    const date = new Date(dateString);
    const month = date.getMonth();
    if (month >= 3 && month <= 5) return 'Q1';
    if (month >= 6 && month <= 8) return 'Q2';
    if (month >= 9 && month <= 11) return 'Q3';
    return 'Q4';
}

function updateStageBreakdown(regionBreakdown, stage, amount) {
    if (!stage) return;
    const existingStage = regionBreakdown.stages.find(s => s.name === stage);
    if (existingStage) {
        existingStage.value += amount;
        existingStage.count++;
    } else {
        regionBreakdown.stages.push({
            name: stage,
            value: amount,
            count: 1
        });
    }
}

function updateRevenueProjection(projection, deal) {
    const amount = parseFloat(deal.Amount) || 0;
    const probability = parseFloat(deal.Probability) || 0;

    if (deal.Stage === 'Closed Won') {
        projection.achieved += amount;
    }

    if (probability >= 80) {
        projection.projected_80 += amount * (probability / 100);
    }
    projection.projected_all += amount * (probability / 100);
}

function isPotentialClosure(deal) {
    const probability = parseFloat(deal.Probability) || 0;
    const stage = deal.Stage || '';
    return probability >= 70 && !stage.toLowerCase().includes('closed');
}

function determineAction(deal) {
    const stage = deal.Stage?.toLowerCase() || '';
    if (stage.includes('proposal')) return 'Follow up on proposal';
    if (stage.includes('negotiation')) return 'Schedule negotiation meeting';
    return 'Review and update';
}

function updateOpportunityTypes(types, dealType, amount) {
    if (!dealType) return;
    dealType = dealType.toUpperCase();
    
    if (dealType.includes('POC')) {
        types.POC.value += amount;
        types.POC.count++;
    } else if (dealType.includes('MAP')) {
        types.MAP.value += amount;
        types.MAP.count++;
    } else if (dealType.includes('GENAI')) {
        types.GenAI.value += amount;
        types.GenAI.count++;
    }
}

// Fetch dashboard data from backend API
export async function getDashboardData() {
  const response = await fetch('http://localhost:5000/api/dashboard-data');
  if (!response.ok) throw new Error('Failed to fetch dashboard data');
  return await response.json();
} 