import React from 'react';
import { Card, CardContent, Typography, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PipelineByStage = ({ data }) => {
    // Transform data for the chart
    const chartData = Object.entries(data.opportunities.by_stage).map(([stage, stageData]) => ({
        name: stage,
        value: stageData.Amount,
        count: stageData['Record Id']
    }));

    // Sort by amount in descending order
    chartData.sort((a, b) => b.value - a.value);

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Pipeline by Stage
                </Typography>
                <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                        <div style={{ width: '100%', height: 300 }}>
                            <ResponsiveContainer>
                                <BarChart data={chartData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                                    <YAxis />
                                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                                    <Legend />
                                    <Bar dataKey="value" fill="#8884d8" name="Pipeline Amount" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <TableContainer component={Paper}>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Stage</TableCell>
                                        <TableCell>Amount</TableCell>
                                        <TableCell>% of Total</TableCell>
                                        <TableCell>Count</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {chartData.map((item, index) => {
                                        const percentage = ((item.value / data.opportunities.total_pipeline) * 100).toFixed(1);
                                        return (
                                            <TableRow key={index}>
                                                <TableCell>{item.name}</TableCell>
                                                <TableCell>${item.value.toLocaleString()}</TableCell>
                                                <TableCell>{percentage}%</TableCell>
                                                <TableCell>{item.count}</TableCell>
                                            </TableRow>
                                        );
                                    })}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default PipelineByStage; 