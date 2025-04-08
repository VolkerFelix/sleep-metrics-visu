document.addEventListener('DOMContentLoaded', () => {
    // Initialize charts
    initializeCharts();
    
    // Load initial data
    loadAnalyticsData();
    
    // Add event listeners
    document.getElementById('period-select').addEventListener('change', loadAnalyticsData);
});

async function loadAnalyticsData() {
    try {
        const period = document.getElementById('period-select').value;
        const data = await sleepMetricsUtils.fetchData(`/analytics/data?period=${period}`);
        updateCharts(data);
        updateInsights(data.insights);
    } catch (error) {
        sleepMetricsUtils.handleError(error);
    }
}

function initializeCharts() {
    // Pattern Analysis Chart
    const patternLayout = {
        title: 'Sleep Pattern Analysis',
        xaxis: { title: 'Time of Day' },
        yaxis: { title: 'Frequency' }
    };
    
    Plotly.newPlot('pattern-chart', [], {
        ...sleepMetricsUtils.chartConfig,
        ...patternLayout
    });

    // Quality Trend Chart
    const qualityTrendLayout = {
        title: 'Sleep Quality Trends',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Score' }
    };
    
    Plotly.newPlot('quality-trend-chart', [], {
        ...sleepMetricsUtils.chartConfig,
        ...qualityTrendLayout
    });

    // Stage Distribution Chart
    const stageDistributionLayout = {
        title: 'Sleep Stage Distribution',
        xaxis: { title: 'Stage' },
        yaxis: { title: 'Percentage' }
    };
    
    Plotly.newPlot('stage-distribution-chart', [], {
        ...sleepMetricsUtils.chartConfig,
        ...stageDistributionLayout
    });

    // Efficiency Chart
    const efficiencyLayout = {
        title: 'Sleep Efficiency Over Time',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Efficiency (%)' }
    };
    
    Plotly.newPlot('efficiency-chart', [], {
        ...sleepMetricsUtils.chartConfig,
        ...efficiencyLayout
    });
}

function updateCharts(data) {
    // Update Pattern Analysis Chart
    const patternTrace = {
        type: 'histogram',
        x: data.sleep_start_times,
        name: 'Sleep Start Times',
        nbinsx: 24,
        histnorm: 'probability'
    };
    
    Plotly.update('pattern-chart', patternTrace);

    // Update Quality Trend Chart
    const qualityTrendTrace = {
        type: 'scatter',
        mode: 'lines+markers',
        x: data.dates,
        y: data.quality_scores,
        name: 'Quality Score'
    };
    
    Plotly.update('quality-trend-chart', qualityTrendTrace);

    // Update Stage Distribution Chart
    const stageDistributionData = [
        {
            type: 'pie',
            labels: ['Deep Sleep', 'REM Sleep', 'Light Sleep'],
            values: [
                data.avg_deep_sleep,
                data.avg_rem_sleep,
                data.avg_light_sleep
            ],
            hole: 0.4
        }
    ];
    
    Plotly.update('stage-distribution-chart', stageDistributionData);

    // Update Efficiency Chart
    const efficiencyTrace = {
        type: 'scatter',
        mode: 'lines+markers',
        x: data.dates,
        y: data.efficiency_scores,
        name: 'Sleep Efficiency'
    };
    
    Plotly.update('efficiency-chart', efficiencyTrace);
}

function updateInsights(insights) {
    const container = document.getElementById('insights-container');
    container.innerHTML = '';
    
    insights.forEach(insight => {
        const insightElement = document.createElement('div');
        insightElement.className = 'insight-card';
        
        insightElement.innerHTML = `
            <h4>${insight.title}</h4>
            <p>${insight.description}</p>
            ${insight.recommendation ? `<p class="recommendation">Recommendation: ${insight.recommendation}</p>` : ''}
        `;
        
        container.appendChild(insightElement);
    });
} 