"""
Client for interacting with the Sleep Data Microservice API.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import requests
from flask import current_app
from requests.exceptions import RequestException


class SleepApiClient:
    """Client for the Sleep Data Microservice API."""

    def __init__(self, base_url: Optional[str] = None, timeout: int = 10):
        """
        Initialize the Sleep API client.

        Args:
            base_url: Base URL for the Sleep API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or current_app.config['SLEEP_API_BASE_URL']
        self.timeout = timeout or current_app.config['SLEEP_API_TIMEOUT']

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make a request to the Sleep API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            API response as a dictionary

        Raises:
            RequestException: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Set default timeout if not provided
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            # Log the error and re-raise
            current_app.logger.error(f"API request failed: {str(e)}")
            raise

    def get_sleep_data(
        self, 
        user_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get sleep data for a specific user and date range.

        Args:
            user_id: User identifier
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            Dictionary containing sleep records and count
        """
        params = {
            'user_id': user_id,
            'limit': limit,
            'offset': offset
        }
        
        if start_date:
            params['start_date'] = start_date.isoformat()
        
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        return self._make_request('GET', '/sleep/data', params=params)

    def get_sleep_analytics(
        self, 
        user_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get sleep analytics for a specific user and date range.

        Args:
            user_id: User identifier
            start_date: Start date for analysis
            end_date: End date for analysis

        Returns:
            Dictionary containing sleep analytics
        """
        params = {
            'user_id': user_id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        return self._make_request('GET', '/sleep/analytics', params=params)

    def generate_dummy_data(
        self, 
        user_id: str, 
        days: int = 30,
        include_time_series: bool = False,
        sleep_quality_trend: Optional[str] = None,
        sleep_duration_trend: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate dummy sleep data for testing.

        Args:
            user_id: User identifier
            days: Number of days to generate data for
            include_time_series: Whether to include time series data
            sleep_quality_trend: Trend for sleep quality
            sleep_duration_trend: Trend for sleep duration

        Returns:
            Dictionary containing generated sleep records
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        payload = {
            'user_id': user_id,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'include_time_series': include_time_series
        }
        
        if sleep_quality_trend:
            payload['sleep_quality_trend'] = sleep_quality_trend
            
        if sleep_duration_trend:
            payload['sleep_duration_trend'] = sleep_duration_trend
        
        return self._make_request('POST', '/sleep/generate', json=payload)
    
    def get_users(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get a list of unique users with their record counts.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            Dictionary containing users list and count
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        
        return self._make_request('GET', '/sleep/users', params=params)