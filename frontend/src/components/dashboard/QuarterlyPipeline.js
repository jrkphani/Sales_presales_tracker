import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import { BarChart } from '../charts/BarChart';

const QuarterlyPipeline = ({ data }) => {
    // Transform data for the chart
    const chartData = data.opportunities.pipeline_by_region_by_quarter.map(item => ({
        name: `${item.YearQuarter} - ${item.Business_Region}`,
        value: item.Amount
    }));

    // Calculate total pipeline by region
    const regionTotals = data.opportunities.pipeline_by_region_by_quarter.reduce((acc, item) => {
        if (!acc[item.Business_Region]) {
            acc[item.Business_Region] = 0;
        }
        acc[item.Business_Region] += item.Amount;
        return acc;
    }, {});

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Quarterly Pipeline by Region
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12} md={8}>
                        <BarChart
                            data={chartData}
                            xAxis="name"
                            yAxis="value"
                            height={400}
                            title="Pipeline by Region and Quarter"
                        />
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Typography variant="subtitle1" gutterBottom>
                            Total Pipeline by Region
                        </Typography>
                        {Object.entries(regionTotals).map(([region, total]) => (
                            <Typography key={region} variant="body2">
                                {region}: ${total.toLocaleString()}
                            </Typography>
                        ))}
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default QuarterlyPipeline; 