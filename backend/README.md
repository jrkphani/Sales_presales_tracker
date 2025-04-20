# Sales Presales Tracker Backend

This is the backend service for the Sales Presales Tracker application. It provides API endpoints for fetching and processing sales data from Zoho CRM.

## Features

- RESTful API endpoints for dashboard data
- Automated data fetching from Zoho CRM using bulk read API
- Data transformation and processing pipeline
- Scheduled data refresh jobs
- Data archiving and backup functionality

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the application:
   ```bash
   python main.py
   ```

## Project Structure

```
backend/
├── app/                      # Application package
│   ├── api/                 # API endpoints and error handlers
│   ├── config/             # Configuration management
│   ├── core/              # Core business logic
│   ├── models/            # Data models
│   └── tasks/             # Scheduled tasks
├── data/                   # Data storage
├── scripts/               # Utility scripts
└── tests/                 # Test suite
```

## API Endpoints

- `GET /api/dashboard-data`: Fetch processed dashboard data
- `POST /api/refresh`: Trigger manual data refresh
- `GET /api/health`: Service health check

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Format code:
   ```bash
   black .
   isort .
   ```

4. Check code quality:
   ```bash
   flake8
   ```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and ensure they pass
4. Submit a pull request

## License

This project is proprietary and confidential. 