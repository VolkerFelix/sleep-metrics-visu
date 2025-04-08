document.addEventListener('DOMContentLoaded', () => {
    // Initialize date inputs with default values
    const today = new Date();
    const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
    
    document.getElementById('start-date').value = lastWeek.toISOString().split('T')[0];
    document.getElementById('end-date').value = today.toISOString().split('T')[0];

    // Initialize charts
    initializeCharts();
    
    // Load initial data
    loadDashboardData();
    
    // Add event listeners
    document.getElementById('update-dashboard').addEventListener('click', loadDashboardData);
});

async function loadDashboardData() {
    try {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        
        const data = await sleepMetricsUtils.fetchData(`/dashboard/data?start_date=${startDate}&end_date=${endDate}`);
        updateCharts(data);
    } catch (error) {
        sleepMetricsUtils.handleError(error);
    }
}

function initializeCharts() {
    // Duration Chart
    const durationTrace = {
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Sleep Duration'
    };
    
    const durationLayout = {
        title: 'Sleep Duration Over Time',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Hours' }
    };
    
    Plotly.newPlot('duration-chart', [durationTrace], {
        ...sleepMetricsUtils.chartConfig,
        ...durationLayout
    });

    // Quality Chart
    const qualityTrace = {
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Sleep Quality'
    };
    
    const qualityLayout = {
        title: 'Sleep Quality Score',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Score (1-100)' }
    };
    
    Plotly.newPlot('quality-chart', [qualityTrace], {
        ...sleepMetricsUtils.chartConfig,
        ...qualityLayout
    });

    // Stages Chart
    const stagesLayout = {
        title: 'Sleep Stages Distribution',
        barmode: 'stack',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Hours' }
    };
    
    Plotly.newPlot('stages-chart', [], {
        ...sleepMetricsUtils.chartConfig,
        ...stagesLayout
    });

    // Trends Chart
    const trendsLayout = {
        title: 'Weekly Sleep Trends',
        xaxis: { title: 'Week' },
        yaxis: { title: 'Average Hours' }
    };
    
    Plotly.newPlot('trends-chart', [], {
        ...sleepMetricsUtils.chartConfig,
        ...trendsLayout
    });
}

function updateCharts(data) {
    // Update Duration Chart
    const durationTrace = {
        x: data.map(d => sleepMetricsUtils.formatDate(d.date)),
        y: data.map(d => d.duration),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Sleep Duration'
    };
    
    Plotly.update('duration-chart', durationTrace);

    // Update Quality Chart
    const qualityTrace = {
        x: data.map(d => sleepMetricsUtils.formatDate(d.date)),
        y: data.map(d => d.quality_score),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Sleep Quality'
    };
    
    Plotly.update('quality-chart', qualityTrace);

    // Update Stages Chart
    const stagesData = [
        {
            x: data.map(d => sleepMetricsUtils.formatDate(d.date)),
            y: data.map(d => d.deep_sleep_duration),
            type: 'bar',
            name: 'Deep Sleep'
        },
        {
            x: data.map(d => sleepMetricsUtils.formatDate(d.date)),
            y: data.map(d => d.rem_sleep_duration),
            type: 'bar',
            name: 'REM Sleep'
        },
        {
            x: data.map(d => sleepMetricsUtils.formatDate(d.date)),
            y: data.map(d => d.light_sleep_duration),
            type: 'bar',
            name: 'Light Sleep'
        }
    ];
    
    Plotly.update('stages-chart', stagesData);

    // Update Trends Chart
    const trendsTrace = {
        x: data.map(d => sleepMetricsUtils.formatDate(d.date)),
        y: data.map(d => d.duration),
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Average Sleep Duration'
    };
    
    Plotly.update('trends-chart', trendsTrace);
} 