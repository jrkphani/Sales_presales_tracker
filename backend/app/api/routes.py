"""
API Routes Module
Defines the API endpoints for the application
"""

from flask import jsonify, request
from app.core.services.dashboard_service import get_dashboard_data
from app.core.services.data_service import trigger_data_refresh
from app.core.utils.helpers import get_service_health

def register_routes(app):
    """Register all API routes with the Flask application"""
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify(get_service_health())

    @app.route('/api/dashboard-data')
    def dashboard_data():
        """Get processed dashboard data"""
        try:
            data = get_dashboard_data()
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/refresh', methods=['POST'])
    def refresh_data():
        """Trigger manual data refresh"""
        try:
            result = trigger_data_refresh()
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500 