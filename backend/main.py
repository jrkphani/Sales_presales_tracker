"""
Sales Presales Tracker Backend Application
Main entry point for the Flask application
"""

from flask import Flask
from app import create_app
from app.tasks.scheduler import init_scheduler

# Create Flask application instance
app = create_app()

# Initialize the task scheduler
scheduler = init_scheduler(app)

if __name__ == "__main__":
    # Start the scheduler
    scheduler.start()
    
    # Run the Flask application
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port) 