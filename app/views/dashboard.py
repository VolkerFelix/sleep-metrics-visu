"""
Dashboard routes for the Sleep Data Visualization application.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify

from app.api.client import SleepApiClient
from app.models.sleep_data import SleepRecord, SleepAnalytics

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
def index():
    """Render the dashboard home page."""
    return render_template('dashboard/index.html', title='Dashboard')


@dashboard_bp.route('/view')
def view():
    """View sleep data dashboard for a user."""
    # Get query parameters
    user_id = request.args.get('user_id')
    days_str = request.args.get('days', current_app.config['DEFAULT_DATE_RANGE_DAYS'])
    
    # Validate input
    if not user_id:
        flash('User ID is required', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        days = int(days_str)
    except ValueError:
        days = current_app.config['DEFAULT_DATE_RANGE_DAYS']
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        # Get sleep data
        client = SleepApiClient()
        sleep_data_response = client.get_sleep_data(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=100
        )
        
        # Process sleep records
        sleep_records = [
            SleepRecord(record) for record in sleep_data_response.get('records', [])
        ]
        
        # Get analytics data
        analytics_response = client.get_sleep_analytics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        sleep_analytics = SleepAnalytics(analytics_response)
        
        return render_template(
            'dashboard/view.html',
            title=f'Sleep Dashboard - {user_id}',
            user_id=user_id,
            days=days,
            sleep_records=sleep_records,
            sleep_analytics=sleep_analytics,
            start_date=start_date,
            end_date=end_date
        )
        
    except Exception as e:
        flash(f"Error retrieving sleep data: {str(e)}", 'danger')
        return redirect(url_for('main.index'))


@dashboard_bp.route('/api/sleep-data')
def api_sleep_data():
    """API endpoint for sleep data for charts."""
    user_id = request.args.get('user_id')
    days_str = request.args.get('days', '30')
    
    try:
        days = int(days_str)
    except ValueError:
        days = 30
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        client = SleepApiClient()
        sleep_data_response = client.get_sleep_data(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=100
        )
        
        # Process sleep records
        sleep_records = [
            SleepRecord(record).to_dict() 
            for record in sleep_data_response.get('records', [])
        ]
        
        # Format data for charts
        chart_data = {
            'dates': [],
            'sleep_quality': [],
            'duration_hours': [],
            'deep_sleep_percentage': [],
            'rem_sleep_percentage': [],
            'light_sleep_percentage': [],
            'heart_rate_avg': [],
        }
        
        for record in sorted(sleep_records, key=lambda x: x['date']):
            chart_data['dates'].append(record['date'])
            chart_data['sleep_quality'].append(record.get('sleep_quality'))
            chart_data['duration_hours'].append(record.get('duration_hours'))
            
            # Add sleep phases data if available
            if 'sleep_phases' in record:
                chart_data['deep_sleep_percentage'].append(record.get('deep_sleep_percentage'))
                chart_data['rem_sleep_percentage'].append(record.get('rem_sleep_percentage'))
                chart_data['light_sleep_percentage'].append(record.get('light_sleep_percentage'))
            
            # Add heart rate data if available
            if 'heart_rate' in record:
                chart_data['heart_rate_avg'].append(record.get('heart_rate', {}).get('average'))
        
        return jsonify(chart_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/record/<record_id>')
def view_record(record_id):
    """View detailed information for a single sleep record."""
    user_id = request.args.get('user_id')
    
    if not user_id or not record_id:
        flash('User ID and Record ID are required', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        # Get sleep data for this user
        client = SleepApiClient()
        sleep_data_response = client.get_sleep_data(
            user_id=user_id,
            limit=100
        )
        
        # Find the specific record
        record = next(
            (r for r in sleep_data_response.get('records', []) if r.get('record_id') == record_id), 
            None
        )
        
        if not record:
            flash(f"Sleep record not found: {record_id}", 'danger')
            return redirect(url_for('dashboard.view', user_id=user_id))
        
        # Process record
        sleep_record = SleepRecord(record)
        
        return render_template(
            'dashboard/record.html',
            title=f'Sleep Record - {sleep_record.date}',
            user_id=user_id,
            record=sleep_record
        )
        
    except Exception as e:
        flash(f"Error retrieving sleep record: {str(e)}", 'danger')
        return redirect(url_for('dashboard.view', user_id=user_id))


@dashboard_bp.route('/analytics')
def analytics():
    """View in-depth sleep analytics."""
    # Get query parameters
    user_id = request.args.get('user_id')
    days_str = request.args.get('days', '30')
    
    # Validate input
    if not user_id:
        flash('User ID is required', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        days = int(days_str)
    except ValueError:
        days = 30
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        # Get analytics data
        client = SleepApiClient()
        analytics_response = client.get_sleep_analytics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        sleep_analytics = SleepAnalytics(analytics_response)
        
        # Get sleep data for charts
        sleep_data_response = client.get_sleep_data(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=100
        )
        
        # Process sleep records
        sleep_records = [
            SleepRecord(record) for record in sleep_data_response.get('records', [])
        ]
        
        return render_template(
            'dashboard/analytics.html',
            title=f'Sleep Analytics - {user_id}',
            user_id=user_id,
            days=days,
            sleep_analytics=sleep_analytics,
            sleep_records=sleep_records,
            start_date=start_date,
            end_date=end_date
        )
        
    except Exception as e:
        flash(f"Error retrieving sleep analytics: {str(e)}", 'danger')
        return redirect(url_for('main.index'))    
@dashboard_bp.route('/api/users')
def api_get_users():
    """API endpoint to get users for dropdown selection."""
    try:
        # Get users using the API client
        client = SleepApiClient()
        response = client.get_users(limit=50)  # Limit to a reasonable number for dropdown
        
        return jsonify(response.get('users', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
