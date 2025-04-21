# Sales and Presales Tracking Dashboard

A full-stack application for tracking sales and presales data with a React frontend and Python backend.

## Project Structure

```
sales-presales-tracker/
├── backend/               # Python backend services
│   ├── app/               # Application package
│   ├── scripts/           # Utility scripts (Python)
│   ├── main.py            # Backend entry point
│   └── requirements.txt   # Backend dependencies
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # Frontend services
│   │   └── styles/       # CSS and styling
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
└── package.json          # Root package.json for workspace management
```

## Setup Instructions

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Install backend dependencies:
   ```bash
   cd ../backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the frontend development server:
   ```bash
   cd ../frontend
   npm start
   ```

4. Start the backend services:
   ```bash
   cd ../backend
   source venv/bin/activate  # If not already activated
   python main.py
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:
```
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
```

## Development

- Frontend runs on http://localhost:3000
- Backend services run on http://localhost:5000

## Available Scripts

- `npm run start:frontend` - Start the frontend development server
- `npm run start:backend` - Start the backend services
- `npm run install:all` - Install dependencies for all workspaces
- `npm run install:frontend` - Install frontend dependencies
- `npm run install:backend` - Install backend dependencies
