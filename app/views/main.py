"""
Main routes for the Sleep Data Visualization application.
"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify

from app.api.client import SleepApiClient

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the home page."""
    return render_template('index.html', title='Sleep Data Visualization')


@main_bp.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About')


@main_bp.route('/generate-dummy-data', methods=['GET', 'POST'])
def generate_dummy_data():
    """Generate dummy sleep data for testing."""
    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            days = int(request.form.get('days', 30))
            include_time_series = request.form.get('include_time_series') == 'on'
            sleep_quality_trend = request.form.get('sleep_quality_trend')
            sleep_duration_trend = request.form.get('sleep_duration_trend')
            
            # Validate input
            if not user_id:
                flash('User ID is required', 'danger')
                return redirect(url_for('main.generate_dummy_data'))
                
            if days < 1 or days > 365:
                flash('Days must be between 1 and 365', 'danger')
                return redirect(url_for('main.generate_dummy_data'))
            
            # Generate data using the API client
            client = SleepApiClient()
            result = client.generate_dummy_data(
                user_id=user_id,
                days=days,
                include_time_series=include_time_series,
                sleep_quality_trend=sleep_quality_trend,
                sleep_duration_trend=sleep_duration_trend
            )
            
            # Redirect to the dashboard with the generated data
            flash(f"Successfully generated {result['count']} sleep records", 'success')
            return redirect(url_for(
                'dashboard.view',
                user_id=user_id,
                days=current_app.config['DEFAULT_DATE_RANGE_DAYS']
            ))
            
        except Exception as e:
            flash(f"Error generating data: {str(e)}", 'danger')
    
    # GET request - show the form
    return render_template(
        'generate_data.html',
        title='Generate Dummy Data'
    )