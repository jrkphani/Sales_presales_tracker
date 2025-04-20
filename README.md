# Sales and Presales Tracking Dashboard

A full-stack application for tracking sales and presales data with a React frontend and Node.js backend.

## Project Structure

```
sales-presales-tracker/
├── backend/               # Node.js backend services
│   ├── src/
│   │   ├── services/     # Zoho integration and other services
│   │   ├── data/         # Data processing and storage
│   │   └── scripts/      # Utility scripts
│   └── package.json      # Backend dependencies
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # Frontend services
│   │   └── styles/       # CSS and styling
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
└── package.json          # Root package.json for workspace management
```

## Setup Instructions

1. Install dependencies:
   ```bash
   npm run install:all
   ```

2. Start the frontend development server:
   ```bash
   npm run start:frontend
   ```

3. Start the backend services:
   ```bash
   npm run start:backend
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
