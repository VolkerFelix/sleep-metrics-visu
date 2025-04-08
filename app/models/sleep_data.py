"""
Data models for sleep metrics.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any, Union


class SleepPhases:
    """Model for sleep phases data."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize sleep phases from dictionary.
        
        Args:
            data: Dictionary containing sleep phases data
        """
        self.deep_sleep_minutes = data.get('deep_sleep_minutes')
        self.rem_sleep_minutes = data.get('rem_sleep_minutes')
        self.light_sleep_minutes = data.get('light_sleep_minutes')
        self.awake_minutes = data.get('awake_minutes', 0)
    
    @property
    def total_minutes(self) -> int:
        """Get total minutes of all sleep phases."""
        return (
            (self.deep_sleep_minutes or 0) +
            (self.rem_sleep_minutes or 0) +
            (self.light_sleep_minutes or 0) +
            (self.awake_minutes or 0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'deep_sleep_minutes': self.deep_sleep_minutes,
            'rem_sleep_minutes': self.rem_sleep_minutes,
            'light_sleep_minutes': self.light_sleep_minutes,
            'awake_minutes': self.awake_minutes,
            'total_minutes': self.total_minutes
        }


class HeartRateData:
    """Model for heart rate data during sleep."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize heart rate data from dictionary.
        
        Args:
            data: Dictionary containing heart rate data
        """
        self.average = data.get('average')
        self.min = data.get('min')
        self.max = data.get('max')
        self.resting = data.get('resting')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'average': self.average,
            'min': self.min,
            'max': self.max,
            'resting': self.resting
        }


class SleepTimeSeriesPoint:
    """Model for a single point in sleep time series data."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize time series point from dictionary.
        
        Args:
            data: Dictionary containing time series point data
        """
        self.timestamp = (
            datetime.fromisoformat(data['timestamp']) 
            if isinstance(data['timestamp'], str) else data['timestamp']
        )
        self.stage = data.get('stage')
        self.heart_rate = data.get('heart_rate')
        self.movement = data.get('movement')
        self.respiration_rate = data.get('respiration_rate')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'stage': self.stage,
            'heart_rate': self.heart_rate,
            'movement': self.movement,
            'respiration_rate': self.respiration_rate
        }


class SleepRecord:
    """Model for a sleep record."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize sleep record from dictionary.
        
        Args:
            data: Dictionary containing sleep record data
        """
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.date = data.get('date')
        
        # Convert string timestamps to datetime objects
        self.sleep_start = (
            datetime.fromisoformat(data['sleep_start']) 
            if isinstance(data['sleep_start'], str) else data['sleep_start']
        )
        self.sleep_end = (
            datetime.fromisoformat(data['sleep_end']) 
            if isinstance(data['sleep_end'], str) else data['sleep_end']
        )
        
        self.duration_minutes = data.get('duration_minutes')
        
        # Process sleep phases if available
        self.sleep_phases = (
            SleepPhases(data['sleep_phases']) 
            if data.get('sleep_phases') else None
        )
        
        self.sleep_quality = data.get('sleep_quality')
        
        # Process heart rate data if available
        self.heart_rate = (
            HeartRateData(data['heart_rate']) 
            if data.get('heart_rate') else None
        )
        
        # Process time series data if available
        self.time_series = (
            [SleepTimeSeriesPoint(point) for point in data['time_series']]
            if data.get('time_series') else []
        )
    
    @property
    def duration_hours(self) -> float:
        """Get sleep duration in hours."""
        return self.duration_minutes / 60 if self.duration_minutes else 0
    
    @property
    def deep_sleep_percentage(self) -> Optional[float]:
        """Get deep sleep as a percentage of total sleep time."""
        if not self.sleep_phases or not self.sleep_phases.deep_sleep_minutes:
            return None
        
        return (self.sleep_phases.deep_sleep_minutes / self.duration_minutes) * 100
    
    @property
    def rem_sleep_percentage(self) -> Optional[float]:
        """Get REM sleep as a percentage of total sleep time."""
        if not self.sleep_phases or not self.sleep_phases.rem_sleep_minutes:
            return None
        
        return (self.sleep_phases.rem_sleep_minutes / self.duration_minutes) * 100
    
    @property
    def light_sleep_percentage(self) -> Optional[float]:
        """Get light sleep as a percentage of total sleep time."""
        if not self.sleep_phases or not self.sleep_phases.light_sleep_minutes:
            return None
        
        return (self.sleep_phases.light_sleep_minutes / self.duration_minutes) * 100
    
    @property
    def awake_percentage(self) -> Optional[float]:
        """Get awake time as a percentage of total sleep time."""
        if not self.sleep_phases or not self.sleep_phases.awake_minutes:
            return None
        
        return (self.sleep_phases.awake_minutes / self.duration_minutes) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'sleep_start': self.sleep_start.isoformat(),
            'sleep_end': self.sleep_end.isoformat(),
            'duration_minutes': self.duration_minutes,
            'duration_hours': self.duration_hours,
            'sleep_quality': self.sleep_quality
        }
        
        # Add sleep phases data if available
        if self.sleep_phases:
            result['sleep_phases'] = self.sleep_phases.to_dict()
            result['deep_sleep_percentage'] = self.deep_sleep_percentage
            result['rem_sleep_percentage'] = self.rem_sleep_percentage
            result['light_sleep_percentage'] = self.light_sleep_percentage
            result['awake_percentage'] = self.awake_percentage
        
        # Add heart rate data if available
        if self.heart_rate:
            result['heart_rate'] = self.heart_rate.to_dict()
        
        # Add time series data if available
        if self.time_series:
            result['time_series'] = [point.to_dict() for point in self.time_series]
        
        return result


class SleepTrend:
    """Model for sleep trend information."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize sleep trend from dictionary.
        
        Args:
            data: Dictionary containing sleep trend data
        """
        self.metric = data.get('metric')
        self.direction = data.get('direction')
        self.strength = data.get('strength')
        self.average_change = data.get('average_change_per_day')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'metric': self.metric,
            'direction': self.direction,
            'strength': self.strength,
            'average_change': self.average_change
        }


class SleepAnalytics:
    """Model for sleep analytics data."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize sleep analytics from dictionary.
        
        Args:
            data: Dictionary containing sleep analytics data
        """
        self.user_id = data.get('user_id')
        self.start_date = data.get('start_date')
        self.end_date = data.get('end_date')
        
        # Process stats
        stats = data.get('stats', {})
        self.average_duration_minutes = stats.get('average_duration_minutes')
        self.average_sleep_quality = stats.get('average_sleep_quality')
        self.average_deep_sleep_minutes = stats.get('average_deep_sleep_minutes')
        self.average_rem_sleep_minutes = stats.get('average_rem_sleep_minutes')
        self.average_light_sleep_minutes = stats.get('average_light_sleep_minutes')
        self.total_records = stats.get('total_records')
        self.date_range_days = stats.get('date_range_days')
        
        # Process trends
        trends_data = data.get('trends', {})
        self.duration_trend = (
            SleepTrend(trends_data['duration_trend']) 
            if trends_data.get('duration_trend') else None
        )
        self.quality_trend = (
            SleepTrend(trends_data['quality_trend']) 
            if trends_data.get('quality_trend') else None
        )
        
        # Process other trend data
        self.schedule_consistency = trends_data.get('schedule_consistency')
        self.duration_variability = trends_data.get('duration_variability')
        
        # Process recommendations
        self.recommendations = data.get('recommendations', [])
    
    @property
    def average_duration_hours(self) -> Optional[float]:
        """Get average sleep duration in hours."""
        return (
            self.average_duration_minutes / 60 
            if self.average_duration_minutes else None
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'user_id': self.user_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'stats': {
                'average_duration_minutes': self.average_duration_minutes,
                'average_duration_hours': self.average_duration_hours,
                'average_sleep_quality': self.average_sleep_quality,
                'average_deep_sleep_minutes': self.average_deep_sleep_minutes,
                'average_rem_sleep_minutes': self.average_rem_sleep_minutes,
                'average_light_sleep_minutes': self.average_light_sleep_minutes,
                'total_records': self.total_records,
                'date_range_days': self.date_range_days
            },
            'recommendations': self.recommendations
        }
        
        # Add trends if available
        result['trends'] = {}
        
        if self.duration_trend:
            result['trends']['duration'] = self.duration_trend.to_dict()
            
        if self.quality_trend:
            result['trends']['quality'] = self.quality_trend.to_dict()
            
        if self.schedule_consistency:
            result['trends']['schedule_consistency'] = self.schedule_consistency
            
        if self.duration_variability:
            result['trends']['duration_variability'] = self.duration_variability
        
        return result