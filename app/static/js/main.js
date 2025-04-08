// Common utility functions
const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
};

const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
};

const formatDuration = (hours) => {
    const wholeHours = Math.floor(hours);
    const minutes = Math.round((hours - wholeHours) * 60);
    return `${wholeHours}h ${minutes}m`;
};

// Error handling
const handleError = (error) => {
    console.error('Error:', error);
    // You could add a toast notification or other UI feedback here
};

// API calls
const fetchData = async (url, options = {}) => {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        handleError(error);
        throw error;
    }
};

// Chart configuration
const chartConfig = {
    responsive: true,
    displayModeBar: false,
    modeBarButtonsToRemove: ['lasso2d', 'select2d']
};

// Export utilities
window.sleepMetricsUtils = {
    formatDate,
    formatTime,
    formatDuration,
    handleError,
    fetchData,
    chartConfig
}; 