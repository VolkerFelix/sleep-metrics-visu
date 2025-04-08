# Sleep Metrics Visualization

A Flask-based web application for visualizing and analyzing sleep metrics data. This application provides interactive dashboards and analytics to help users understand their sleep patterns and improve their sleep quality.

## Features

- Interactive sleep metrics dashboard
- Detailed sleep stage analysis
- Sleep quality tracking
- Trend analysis and insights
- Responsive design for all devices

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sleep-metrics-visu.git
cd sleep-metrics-visu
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration settings.

## Running the Application

1. Start the Flask development server:
```bash
python run.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

## Project Structure

```
├── app/
│   ├── __init__.py              # Flask application initialization
│   ├── config.py                # Configuration settings
│   ├── api/                     # API client for sleep data
│   ├── models/                  # Data models
│   ├── static/                  # Static files (CSS, JS, images)
│   ├── templates/               # Jinja2 templates
│   └── views/                   # Route handlers
├── requirements.txt             # Project dependencies
├── run.py                       # Application entry point
└── README.md                    # Project documentation
```

## API Integration

The application integrates with a sleep data microservice to fetch sleep metrics. Configure the API endpoint in your `.env` file:

```
SLEEP_API_URL=http://your-api-endpoint/api
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- Plotly for interactive visualizations
- SQLAlchemy for database operations
