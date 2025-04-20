"""
Error Handlers Module
Defines custom error handlers for the API
"""

from flask import jsonify

def register_error_handlers(app):
    """Register error handlers with the Flask application"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors"""
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        return jsonify({
            'error': 'Unexpected Error',
            'message': str(error)
        }), 500 