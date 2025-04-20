import React from 'react';
import { Card, CardContent, Typography, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const HighProbabilityOpportunities = ({ data }) => {
    // Calculate high probability opportunities (stages with 80 or 90)
    const highProbabilityStages = Object.entries(data.opportunities.by_stage)
        .filter(([stage]) => stage.includes('(80)') || stage.includes('(90)'));
    
    const totalHighProbabilityPipeline = highProbabilityStages
        .reduce((sum, [_, data]) => sum + data.Amount, 0);
    
    // Calculate POC/MAP/GenAI opportunities
    const pocStages = Object.entries(data.opportunities.by_stage)
        .filter(([stage]) => stage.toLowerCase().includes('poc'));
    const mapStages = Object.entries(data.opportunities.by_stage)
        .filter(([stage]) => stage.toLowerCase().includes('map'));
    const genaiStages = Object.entries(data.opportunities.by_stage)
        .filter(([stage]) => stage.toLowerCase().includes('genai'));
    
    const totalPocPipeline = pocStages.reduce((sum, [_, data]) => sum + data.Amount, 0);
    const totalMapPipeline = mapStages.reduce((sum, [_, data]) => sum + data.Amount, 0);
    const totalGenaiPipeline = genaiStages.reduce((sum, [_, data]) => sum + data.Amount, 0);
    
    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    High Probability Opportunities
                </Typography>
                <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                        <Typography variant="subtitle1" gutterBottom>
                            Summary
                        </Typography>
                        <Typography variant="body2">
                            Total High Probability Pipeline: ${totalHighProbabilityPipeline.toLocaleString()}
                        </Typography>
                        <Typography variant="body2">
                            Number of High Probability Stages: {highProbabilityStages.length}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <Typography variant="subtitle1" gutterBottom>
                            POC/MAP/GenAI Opportunities
                        </Typography>
                        <Typography variant="body2">
                            Total POC Pipeline: ${totalPocPipeline.toLocaleString()}
                        </Typography>
                        <Typography variant="body2">
                            Total MAP Pipeline: ${totalMapPipeline.toLocaleString()}
                        </Typography>
                        <Typography variant="body2">
                            Total GenAI Pipeline: ${totalGenaiPipeline.toLocaleString()}
                        </Typography>
                    </Grid>
                    <Grid item xs={12}>
                        <TableContainer component={Paper}>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Stage</TableCell>
                                        <TableCell>Amount</TableCell>
                                        <TableCell>Number of Opportunities</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {highProbabilityStages.map(([stage, data], index) => (
                                        <TableRow key={index}>
                                            <TableCell>{stage}</TableCell>
                                            <TableCell>${data.Amount.toLocaleString()}</TableCell>
                                            <TableCell>{data['Record Id']}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default HighProbabilityOpportunities; 